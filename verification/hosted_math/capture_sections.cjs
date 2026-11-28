'use strict';
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const {chromium}=require('playwright');
const {waitForHostedMath,VIEWPORTS}=require('./capture_hosted_math.cjs');
const inventory=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const sections=JSON.parse(fs.readFileSync(process.argv[4],'utf8'));
const out=process.argv[3];
fs.mkdirSync(out);
const receipts=[];
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  await Promise.all(VIEWPORTS.map(async viewport=>{
   const context=await browser.newContext({viewport,deviceScaleFactor:1,colorScheme:'light'});
   try {
    for(const [sourcePath,titles] of Object.entries(sections)){
     const source=inventory.pages.find(p=>p.path===sourcePath);
     const page=await context.newPage();
     try {
      const visit=async()=>{
       const res=await page.goto(source.url,{waitUntil:'domcontentloaded',timeout:60000});
       if(!res||page.url()!==source.url||res.url()!==source.url||res.request().redirectedFrom()!==null) throw Error('Navigation did not preserve exact pinned source URL');
       return res.status();
      };
      let status=await visit();const first=status;
      for(const delay of [1000, 4000, 8000, 15000]) {
       if(![502,503,504].includes(status)) break;
       await page.waitForTimeout(delay);
       status=await visit();
      }
      if(status!==200)throw Error('HTTP '+status+' on '+sourcePath);
      const article=page.locator('article.markdown-body').first();
      await article.waitFor({state:'visible',timeout:30000});
      await page.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=900){window.scrollTo({left:0,top:y,behavior:'instant'});await new Promise(resolve=>setTimeout(resolve,40));}});
      await waitForHostedMath(article,source.expressions.length);
      for(const title of titles){
       const heading=article.getByRole('heading',{name:title,exact:true});
       if(await heading.count()!==1)throw Error('Expected one heading for '+title);
       const visible=await heading.evaluate(el=>{
        const y=el.getBoundingClientRect().top+scrollY;
        window.scrollTo({left:0,top:y-240,behavior:'instant'});
        const rect=el.getBoundingClientRect();const at=document.elementFromPoint(rect.left+24,rect.top+rect.height/2);
        return {top:rect.top,left:rect.left,width:rect.width,height:rect.height,unoccluded:at===el||el.contains(at)};
       });
       if(!visible.unoccluded||visible.top<0||visible.top+visible.height>viewport.height)throw Error('Heading occluded '+title);
       const filename=`${title.toLowerCase().replace(/[^a-z]+/g,'-')}-${viewport.width}.png`;
       const target=path.join(out,filename);await page.screenshot({path:target,fullPage:false});
       receipts.push({viewport,path:source.path,url:source.url,revision:inventory.revision,source_sha256:source.source_sha256,title,visible,first_status:first,screenshot:filename,screenshot_sha256:crypto.createHash('sha256').update(fs.readFileSync(target)).digest('hex'),observed_at:new Date().toISOString()});
      }
     } finally {await page.close();}
    }
   } finally {await context.close();}
  }));
 } finally {await browser.close();fs.writeFileSync(path.join(out,'receipts.json'),JSON.stringify(receipts,null,2)+'\n');}
})().catch(e=>{console.error(e);process.exitCode=1;});
