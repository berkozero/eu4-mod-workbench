// Optional browser QA. Uses public Playwright APIs; never starts EU4.
const {chromium}=require('playwright');
const fs=require('fs'),path=require('path'),assert=require('assert');
(async()=>{
 const file=path.resolve(process.argv[2]||'dist/teutonic/preview.html');
 const D=JSON.parse(fs.readFileSync(path.join(path.dirname(file),'preview-data.json')));
 const options={headless:true};if(process.env.PLAYWRIGHT_CHANNEL)options.channel=process.env.PLAYWRIGHT_CHANNEL;
 const browser=await chromium.launch(options),page=await browser.newPage({viewport:{width:1600,height:1080}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));await page.goto(require('url').pathToFileURL(file).href);
 await page.locator('#reset').click();assert.equal(await page.locator('.mission').count(),D.missions.length);
 assert.equal(await page.locator('.paths > path').count(),D.missions.reduce((n,m)=>n+m.arrowParents.length,0));
 for(const m of D.missions){
  await page.evaluate(id=>chooseMission(id,'conditions',false),m.id);
  assert((await page.locator('#detail').innerText()).includes(m.title));
  assert(await page.locator(`[data-rewards-for="${m.id}"]`).isVisible());
  for(const missing of m.checklistParents){
   await page.evaluate(({id,parents,missing,path})=>{state.done=[path,...parents.filter(p=>p!==missing)].filter(p=>p&&p!==id&&p!==missing);chooseMission(id,'conditions',false);markComplete(id)},{id:m.id,parents:m.parents,missing,path:D.pathChoiceMission});
   assert(!(await page.evaluate(id=>state.done.includes(id),m.id)));
  }
 }
 // Exercise branch/path and counted alternative milestones when this project has them.
 for(const m of D.missions.filter(m=>m.triggerAST.some(([k,v])=>k==='calc_true_if'&&v.every(([key])=>['mission_completed','amount'].includes(key))))){
  const gate=m.triggerAST.find(([k])=>k==='calc_true_if')[1];const candidates=gate.filter(([k])=>k==='mission_completed').map(([,id])=>D.missions.find(m=>m.scriptId===id).id);const amount=+gate.find(([k])=>k==='amount')[1];
  await page.evaluate(({m,path,candidates,amount})=>{state.done=[path,...m.parents,...candidates.slice(0,amount-1)].filter(Boolean);chooseMission(m.id,'conditions',false);markComplete(m.id)},{m,path:D.pathChoiceMission,candidates,amount});
  assert(!(await page.evaluate(id=>state.done.includes(id),m.id)));
 }
 await page.locator('[data-view="sequence"]').click();assert.equal(await page.locator('.sequenceRow').count(),D.missions.length);
 await page.locator('[data-view="decisions"]').click();assert.equal(await page.locator('.decisionRow').count(),D.decisions.length);
 for(const event of Object.values(D.events)){
  await page.evaluate(id=>showEvent(id),event.id);assert((await page.locator('#eventBody').innerText()).includes(event.title));
  for(const option of event.options)assert((await page.locator('#eventBody').innerText()).includes(option.label));
  await page.evaluate(()=>document.querySelector('#eventDialog').close());
 }
 await page.locator('#reset').click();await page.locator('[data-view="tree"]').click();
 assert.equal(await page.locator('img').evaluateAll(xs=>xs.filter(i=>!i.complete||!i.naturalWidth).length),0);
 assert.deepEqual(errors,[]);await page.screenshot({path:path.join(path.dirname(file),'preview-verified.png')});
 console.log(JSON.stringify({missions:D.missions.length,all_reward_panels:true,checklist_gates:true,events:Object.keys(D.events).length,broken_images:0,javascript_errors:errors,game_launched:false},null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
