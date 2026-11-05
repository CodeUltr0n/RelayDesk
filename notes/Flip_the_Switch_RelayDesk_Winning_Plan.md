# **FLIP THE SWITCH HACKATHON** 

A focused, judge-oriented execution plan for a solo builder 

PROJECT: RELAYDESK 

Evidence-gated customer support triage and engineering escalation 

**Hackathon:** 4–7 November 2026 **Personal deadline:** 6 November 2026 

**Target track:** Best Business Workflow **Target prize:** $2,000 

### **The plan in one sentence** 

Build a reliable workflow in which a human and Switch-connected agents decide whether a customer issue should be answered, clarified, marked as a duplicate, or escalated—with ranked evidence and verification for technical fixes. 

**Important constraint: you are going home on 7 November. This plan treats 6 November as the hard build, demo, and submission deadline. Do not rely on the official 7 November cutoff.** 

Prepared 23 October 2026 • For planning, not a guarantee of winning 

**RELAYDESK | FLIP THE SWITCH HACKATHON** 

## **1. Strategy: build for the rubric** 

No project can guarantee a win. The highest-probability strategy is a narrow workflow that runs end-to-end, uses Switch as a real collaboration layer, proves its decisions with a small benchmark, and is easy for judges to reproduce. 

|**Judging criterion**|**Weight**|**What to demonstrate**|
|---|---|---|
|**Use of Switch**|**30%**|Shared room contains human request, evidence, agent handoff, approval and final case record. If<br>Switch is removed, the collaboration workflow breaks.|
|**Technical execution**|**25%**|Fresh setup works; tests pass; decisions are explainable; timeouts and failure states are handled;<br>repository is reproducible.|
|**Creativity and impact**|**25%**|Reduce unnecessary engineering escalations while protecting recall for real bugs. Show<br>measured trade-offs rather than broad claims.|
|**Presentation and**<br>**documentation**|**20%**|A crisp two-case demo, concise README, clear architecture and honest benchmark.|



### **Why not a generic incident-response bot?** 

The official Switch materials already showcase a triage/reproduction template and an incident/release workflow. RelayDesk should differentiate itself through evidence-gated support decisions: answer, clarify, deduplicate, or escalate. Keep the reproducible-fix path as a conditional branch, not the whole product. 

### **Product promise** 

_“RelayDesk helps support teams resolve routine issues responsibly and send the right technical issues to engineering—with evidence for every decision.”_ 

Do not claim production-grade savings. The first benchmark is synthetic and exploratory; use it to demonstrate the method, disclose limits, and invite real-world validation. 

Prepared 23 Oct 2026 • Solo plan • Target: submit by 6 Nov 

Page 2 

**RELAYDESK | FLIP THE SWITCH HACKATHON** 

## **2. Product workflow and architecture** 

**1. Human report** — A support lead posts a synthetic issue in the Switch-connected team room. 

**2. Triage** — Agent restates the issue, classifies it and identifies missing information. 

**3. Shortlist** — Deterministic retrieval selects a small set of matching past tickets, runbooks, release notes, logs and tests. 

**4. Score** — Each candidate receives a visible score based on symptom/error match, component/version match, release timing and direct reproduction evidence. 

**5. Decide** — Choose a supported draft response, clarification request, duplicate candidate or engineering escalation. 

**6. Conditional investigation** — For a credible new bug, an investigator and coding/QA agent coordinate through the shared room. 

**7. Verify and approve** — Reproduce and test in an isolated copy; a human approves the response or handoff. 

**8. Case report** — Post the outcome, evidence, tests, uncertainties and human decision back into the room. 

### **Initial evidence scoring (hypothesis to test)** 

|**Feature**|**Initial weight**|**Meaning**|
|---|---|---|
|**Error/symptom match**|**35%**|Does the evidence show the same observable failure?|
|**Component/version match**|**25%**|Does it affect the same service or version?|
|**Release/change timing**|**20%**|Did the failure appear around a relevant change?|
|**Reproduction/test evidence**|**20%**|Is there a direct reproduction or test result?|



These weights are starting values, not validated optimal weights. Scores rank candidates; they are not calibrated probabilities. Tune on development cases only, then report results on held-out cases. 

### **Core implementation choices** 

- **Switch:** shared room, explicit agent roles and visible handoffs; use documented Switch room configuration and protocol. 

- **Agent:** OpenCode through Switch Console; use the model that passes your own tool-use tests, not the model with the most impressive marketing. 

- **Model budget:** try a local/Ollama model first if it works on your Mac M1; retain a documented provider fallback if local tool calling is unreliable. 

- **Decision engine:** Python 3.11+, deterministic retrieval/scoring/routing, pytest. 

- **Data:** synthetic tickets, runbooks, releases, logs and a deliberately buggy sample service. 

- **Chat:** try Discord; if its bridge blocks the core build for 60–90 minutes, use Switch's bundled Mattermost and keep building. 

- **Optional MCP layer:** expose existing Python functions after the end-to-end flow works. Do not let MCP integration delay the core submission. 

Prepared 23 Oct 2026 • Solo plan • Target: submit by 6 Nov 

Page 3 

**RELAYDESK | FLIP THE SWITCH HACKATHON** 

## **3. Repository structure and test plan** 

`relaydesk/` III `README.md` III `pyproject.toml` III `.env.example` III `config/policy.yaml` III `src/relaydesk/` I III `schemas.py` I III `normalize.py` I III `retrieval.py` I III `scoring.py` I III `decision.py` I III `handoff.py` I III `sandbox.py` I III `mcp_server.py` III `fixtures/` I III `tickets/ runbooks/ releases/ logs/` I III `buggy_service/` III `tests/` I III `test_retrieval.py` I III `test_scoring.py` I III `test_decision.py` I III `test_sandbox.py` I III `test_end_to_end.py` III `scripts/run_eval.py` III `docs/` 

III `architecture.md` III `evaluation.md` III `safety.md` III `demo-script.md` 

### **Required test scenarios** 

|**Case**|**Expected behavior**|
|---|---|
|**Known duplicate**|Finds related case, shows evidence and suggests duplicate handling; does not invent certainty.|
|**Answerable runbook question**|Returns a draft grounded in a cited runbook section; human can approve.|
|**Missing information**|Asks a targeted clarifying question instead of guessing.|
|**Novel technical regression**|Escalates with relevant evidence and invokes the investigation path.|
|**Patch fails tests**|Reports failure and rejects the proposed fix; never claims resolution.|
|**Malicious instruction inside a log**|Treats log content as untrusted data; does not follow embedded instructions.|
|**Timeout or agent unavailable**|Posts a failure state and gives the human a safe next step.|



### **Safety boundary** 

- Use synthetic cases; no real customer data or secrets in the repository or recording. 

- Keep investigation read-only. Run tests in a disposable copy, use fixed commands and timeouts, and disable network access where practical. 

Prepared 23 Oct 2026 • Solo plan • Target: submit by 6 Nov 

Page 4 

**RELAYDESK | FLIP THE SWITCH HACKATHON** 

- Never give the demo production deployment or rollback credentials. 

- Require explicit human approval before sending customer-facing messages or accepting patches. 

- Treat tickets, logs, external text and agent-generated summaries as untrusted input. 

Prepared 23 Oct 2026 • Solo plan • Target: submit by 6 Nov 

Page 5 

**RELAYDESK | FLIP THE SWITCH HACKATHON** 

## **4. Execution calendar: finish by 6 November** 

The official event runs 4–7 November, but your personal deadline is the evening of 6 November. Plan to submit a stable version before travel day; do not rely on the official final-day deadline. 

|**Date**|**Focus**|**Must finish by end of day**|
|---|---|---|
|**Oct 23–24**|Scope + environment|Read rules/resources, verify eligibility, install Docker/Switch Console/OpenCode, prove<br>one agent can answer through Switch.|
|**Oct 25–26**|Model smoke tests|Try five repeatable tasks: structured output, tool use, evidence reading, file edit, test run.<br>Pick the most reliable provider.|
|**Oct 27–28**|Integration confidence|Read room permissions, agent protocol, bridge and safety docs. Test Discord path and<br>know Mattermost fallback.|
|**Oct 29–Nov 1**|Planning only|Write the build checklist, draft benchmark cases and demo outline. Avoid prebuilding the<br>submitted workflow; follow event rules.|
|**Nov 2**|Kickoff|Kickoff listed 3:30 PM UTC / 9:00 PM IST. Check for rule or resource changes.|
|**Nov 3**|Freeze scope|Choose chat fallback, model fallback and exact must-have features. Prepare a<br>time-boxed checklist.|
|**Nov 4**|Vertical slice|Build the Switch room and agents during the hackathon; human submits one case, triage<br>responds, handoff/return path works.|
|**Nov 5**|Evidence decisions|Add retrieval, shortlist, scoring, four outcomes and explanations. Ensure every result<br>points to evidence.|
|**Nov 6 morning**|Verification + evaluation|Add isolated repro/test and human approval; run held-out benchmark; fix only critical<br>failures.|
|**Nov 6 afternoon**|Release candidate|Fresh-clone test, README, architecture/safety/evaluation docs, final demo recording,<br>check secrets and licences.|
|**Nov 6 by 8 PM IST**|SUBMIT|Submit repo, README and video. Verify the submission is received and preserve a local<br>backup before travel.|



**Hard stop: no new features after 12 PM IST on November 6 unless a core path is broken. Aim for submission by 8 PM IST, with 9 PM as an absolute internal cutoff.** 

Prepared 23 Oct 2026 • Solo plan • Target: submit by 6 Nov 

Page 6 

**RELAYDESK | FLIP THE SWITCH HACKATHON** 

## **5. Evaluation: prove the workflow helps** 

Create 40 labelled synthetic support cases if time allows: known/duplicate issues, answerable runbook questions, missing-information cases, and new technical bugs. Keep a development split for tuning and a held-out split for final reporting. 

|**Metric**|**What it measures**|**How to report it**|
|---|---|---|
|**Correct next action**|Whether the chosen answer/clarify/duplicate/escalate<br>action matches the label.|Correct cases / all held-out cases; include error<br>examples.|
|**Escalation precision**|How many engineering escalations really needed<br>engineering.|True bug escalations / all escalations.|
|**Escalation recall**|How many true technical bugs were caught.|True bug escalations / all true bugs.|
|**Top-3 evidence recall**|Whether relevant evidence appears in the shortlist.|Cases with relevant evidence in top 3 / eligible<br>cases.|
|**Unsupported assertions**|Claims about cause/fix without supporting evidence.|Count and representative examples.|
|**Test success + cost**|Patch/test outcomes, tool calls and elapsed time.|Report failures, latency and calls; do not<br>cherry-pick.|



### **Baselines to compare** 

- **Baseline:** one-shot triage agent makes a decision without the shortlist/score/decision pipeline. 

- **RelayDesk:** deterministic evidence retrieval, score, explicit routing, conditional investigation and human approval. 

- Use the same cases for both, keep the held-out set untouched during tuning, and report where RelayDesk is worse as well as where it is better. 

### **Three-minute demo script** 

|**Time**|**What judges see**|**Narration**|
|---|---|---|
|**0:00–0:20**|Title and shared room|“Support teams either escalate too much or miss real bugs. RelayDesk uses<br>evidence to choose the next responsible action.”|
|**0:20–1:05**|Known duplicate / answerable issue|Show shortlist, score breakdown, cited source and proposed action.|
|**1:05–2:10**|Novel synthetic regression|Show agent handoff in Switch, evidence, isolated reproduction/test and<br>actual result.|
|**2:10–2:40**|Human approval + final case record|Explain why the shared room is the coordination/audit layer, not just a<br>notification feed.|
|**2:40–3:00**|Real benchmark summary|Show actual metrics and one limitation; label data synthetic.|



Prepared 23 Oct 2026 • Solo plan • Target: submit by 6 Nov 

Page 7 

**RELAYDESK | FLIP THE SWITCH HACKATHON** 

## **6. Submission checklist and contingency plan** 

### **Product and Switch** 

- I At least one human and one agent complete a real task through Switch. 

- I The shared room visibly carries the request, evidence, agent handoff, decision and final report. 

- I Agent roles, addressing permissions and room setup are documented. 

- I Discord works, or the documented Mattermost fallback is used and limitations are stated. 

### **Engineering** 

- I Fresh checkout setup instructions have been followed successfully. 

- I Unit tests and end-to-end tests pass; failures and timeouts are handled. 

- I Sandbox patch/reproduction path cannot access production systems. 

- I No API keys, tokens, private data or personal information in Git history or video. 

- I Third-party licences and use of existing templates are respected. 

### **Evidence and presentation** 

- I Benchmark results are generated by the committed evaluation script. 

- I README explains the problem, architecture, how Switch is used, setup, tests and limitations. 

- I Demo shows two contrasting cases and actual tool/test outcomes. 

- I Video is recorded and replayed once before submission. 

- I Submission receipt and a backup copy are saved by 8 PM IST on Nov 6. 

### **Fallback decision tree** 

|**If this happens…**|**Do this…**|
|---|---|
|**Discord integration consumes 60–90**<br>**minutes**|Switch to bundled Mattermost; keep the Switch room workflow and continue.|
|**Local model fails tool calls**|Use a reliable available provider if permitted and available; do not spend half a day tuning a<br>weak local model.|
|**MCP server integration breaks**|Keep the deterministic Python functions and documented agent workflow; make MCP<br>optional, not a blocker.|
|**Patch generation is unreliable**|Keep reproduction and test reporting; demonstrate an evidence-backed escalation and a<br>rejected failing patch.|
|**Time is running out**|Drop the UI, extra integrations and advanced ranking. Preserve the complete Switch flow,<br>tests, README and demo.|



### **Don't do these** 

- Do not copy the hackathon starter template and simply rename it. 

- Do not claim benchmark gains before running the evaluation. 

- Do not use real customer data or grant production access. 

- Do not keep adding agents or integrations when the end-to-end flow is still fragile. 

- Do not leave submission until 7 November. 

Prepared 23 Oct 2026 • Solo plan • Target: submit by 6 Nov 

Page 8 

**RELAYDESK | FLIP THE SWITCH HACKATHON** 

## **7. After the event: roadmap through 2027** 

|**Period**|**Focus**|**Evidence of progress**|
|---|---|---|
|**Nov 2026**|Publish reproducible project and honest benchmark.|Public repo, setup guide, demo, limitations and initial<br>user feedback.|
|**Dec 2026**|Add one real issue-tracker connector only if the core<br>remains reliable.|Permissioned integration with a clear audit trail and<br>tests.|
|**Jan–Mar 2027**|Validate on opt-in anonymized cases; refine policy,<br>evidence quality and evaluation.|Documented failure analysis and repeatable<br>evaluation.|
|**Apr–Jun 2027**|Explore team pilots, configurable policies and measured<br>impact.|User interviews, pilot feedback and defensible impact<br>metrics.|



### **Potential side prizes** 

- **Best Blog:** after the project is stable, write a practical, reproducible build article covering Switch setup, the evidence-gated workflow, what failed and what the benchmark actually showed. 

- **#HowISwitch:** share one clean post and short clip using the official hashtag; do not spam. 

- **Code with Wispr:** only pursue this if you genuinely build using Wispr Flow and can provide the required usage scorecard. It is optional and should not threaten the main track. 

## **8. Official references** 

- **Hackathon overview, track, rubric and FAQs** 

https://www.wemakedevs.org/hackathons/switch 

- **Official schedule and submission deadline** 

https://www.wemakedevs.org/hackathons/switch/schedule 

- **Official resources and quickstart** 

https://www.wemakedevs.org/hackathons/switch/resources 

- **Official rules** 

https://www.wemakedevs.org/hackathons/switch/rules 

- **DevTools Academy overview and judging** 

https://www.devtoolsacademy.com/hackathons/flip-the-switch 

- **Switch source and releases** 

https://github.com/sandbox-quantum/switch 

- **OpenCode model/provider docs** 

- https://opencode.ai/docs/models 

Recheck official docs at kickoff. Integration details, releases and model availability may change before November 4. This plan is based on information available on 23 October 2026 and cannot guarantee a prize. 

**Winning principle: fewer features, stronger proof. Make Switch indispensable, show the evidence behind every decision, verify outcomes, and submit a stable project before travel day.** 

Prepared 23 Oct 2026 • Solo plan • Target: submit by 6 Nov 

Page 9 

