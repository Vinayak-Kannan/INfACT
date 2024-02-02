# INfACT

### Flow
1. Scraping
   2. Scrape LinkedIn (Not in this Repo)
   3. Scrape Courses from vergil (right now very ad-hoc / brittle due to lack of API) - ColumbiaVergilBrowserScrapeScript.js
   4. Minimum needed for scraping is Course / Job Name and a Description
2. (For each 'comparison set', e.g., Columbia vs Industry, Columbia vs MIT vs Industry, NYU vs Columbiaetc.)...
   3. Pass course / job title and description / syllabus through LLM to extract top 5 skills-terms (e.g., knowledge, skill, abilities) for each cluster via LLM by sending each data point to model - get_skills in ParseData.py
   4. Convert skills to embeddings - collapse_rows
   5. Cluster embeddings using HDBScan - Playground.py (HDBScan related code)
   6. Create a table containing the following information
      7. Skill-term, Number of data points (e.g., courses) that have that skill-term, Number of jobs that have skill-term, Other information as needed
3. Create a visualization of the clusters in Tableau