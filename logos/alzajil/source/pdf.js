const { chromium } = require('playwright');
const fs=require('fs');
(async () => {
  const b = await chromium.launch();
  const jobs=fs.readFileSync('jobs.txt','utf8').trim().split('\n').map(l=>l.split(' '));
  for (const [n,w,h] of jobs){
    const p = await b.newPage();
    await p.goto('file://'+process.cwd()+'/html/'+n+'.html');
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({path:'pdf/'+n+'.pdf', width:w+'px', height:h+'px', printBackground:true, pageRanges:'1'});
    await p.close();
  }
  await b.close();
})();
