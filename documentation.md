

# https://developers.google.com/tech-writing

https://university.gitlab.com/courses/gitlab-technical-writing-fundamentals


# SysReptor

Hack The Box (HTB) Academy



# Obsidian — build a personal security knowledge base in Markdown


Draw.io / Lucidchart  - network diagrams and incident flowcharts



| **No.** | **Platform**                                | **What It Offers**                                                                                                  |
| :-----: | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
|  **1**  | Grammarly                                   | Provides real-time grammar, spelling, clarity, and tone suggestions to improve writing.                             |
|  **2**  | Hemingway Editor                            | Highlights complex sentences, passive voice, adverbs, and provides a readability score.                             |
|  **3**  | BBC Learning English                        | Offers free English lessons, grammar, vocabulary, pronunciation, and listening practice for all proficiency levels. |
|  **4**  | Coursera – *English for Career Development* | Free-to-audit course focused on professional English communication, writing, and workplace skills.                  |
|  **5**  | Khan Academy                                | Covers grammar fundamentals, punctuation, sentence structure, and writing basics through free lessons.              |

# BBC Learning English
https://www.bbc.co.uk/learningenglish/


# Gamified Writing Platforms
https://writeandimprove.com/



| **No.** | **Platform**    | **How It's Like a Game**                                                                                     | **Best For**                                                               |
| :-----: | --------------- | ------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
|  **1**  | 4thewords       | RPG-style writing adventure where you defeat monsters by reaching word-count goals within a time limit.      | Building writing speed, consistency, and a daily writing habit.            |
|  **2**  | Frankenstories  | Multiplayer writing game where players quickly contribute story lines and vote for the best entries.         | Fun, collaborative, and fast-paced creative writing practice.              |
|  **3**  | Write & Improve | Automatically scores your writing using CEFR levels and encourages improvement through repeated submissions. | English learners seeking instant feedback and measurable progress.         |
|  **4**  | Groovelit       | Rewards users with points for using proper grammar, descriptive language, and effective writing techniques.  | Students practicing grammar and improving writing quality.                 |
|  **5**  | Write or Die    | Productivity tool that penalizes you for stopping, encouraging continuous writing without hesitation.        | Overcoming procrastination, writer's block, and improving writing fluency. |
















------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

 A good report usually includes scope, methodology, findings, risk rating, evidence, and actionable fixes. [eadteste.fdsm.edu](https://eadteste.fdsm.edu.br/archive-ga-23-31/Book?docid=iRT22-8881&title=how-to-write-a-vulnerability-assessment-report.pdf)

## Report structure

Use this order:

1. Executive summary.
2. Scope and methodology.
3. Tools used.
4. Findings summary.
5. Detailed findings.
6. Remediation plan.
7. Appendix with raw tool output or screenshots.

This structure matches common guidance for vulnerability reports and templates, including a clear scope, analysis, prioritization, and remediation workflow.

## How to combine multiple tools

Different tools often report the same issue in different ways, so the key is to normalize them into one finding record. For each result, capture:

- Asset or host.
- Port or service.
- Vulnerability title.
- Severity.
- Evidence.
- Source tool.
- CVE or reference if available.
- Recommended fix.

That makes it easier to deduplicate overlapping results from multiple scanners and present one clean report.
## Simple demo

### Input from tools

- Nessus: “TLS 1.0 enabled on 10.0.0.5:443.”
- OpenVAS: “Outdated OpenSSL on 10.0.0.5.”
- Nmap: “443/tcp open https.”
- Qualys: “Weak TLS configuration on web server.”

### Normalized finding

| Asset | Finding | Severity | Evidence | Sources | Fix |
|---|---|---:|---|---|---|
| 10.0.0.5 | Weak TLS configuration allowing legacy protocols | High | TLS 1.0 detected on 443 | Nessus, OpenVAS, Qualys | Disable TLS 1.0/1.1, allow TLS 1.2+ only, update OpenSSL |

### Report wording example

**Finding title:** Weak TLS configuration on web server  
**Description:** The server supports legacy TLS protocols that may expose users to downgrade or interception risk.  
**Impact:** An attacker could weaken secure communications and increase the risk of credential or session theft.  
**Recommendation:** Disable legacy protocols, update the crypto library, and re-test after changes. 
## Demo template

You can reuse this format for each finding:

**Title:**  
**Asset:**  
**Tools:**  
**Severity:**  
**Description:**  
**Evidence:**  
**Impact:**  
**Recommendation:**  
**Status:** Open / Fixed / Needs retest

## Best practice

Write the executive summary last, even though it appears first, so it reflects the final findings accurately. Also, keep the language short and clear, and avoid copying raw scanner output directly into the report.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
