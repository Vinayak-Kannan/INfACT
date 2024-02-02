# INfACT

### Flow
1. Scraping
   2. Scrape LinkedIn (Not in this Repo)
   3. Scrape Courses from vergil (right now very ad-hoc / brittle due to lack of API)
   4. Minimum needed for scraping is Course / Job Name and a Description
2. (For each 'comparison set', e.g., Columbia vs Industry, Columbia vs MIT vs Industry, NYU vs Columbiaetc.)...
   3. Convert text to embeddings
   3. Cluster embeddings using HDBScan
   4. Create up to 5 skills-terms (e.g., knowledge, skill, abilities) for each cluster via LLM by sending each data point to model
   5. Create a table containing the following information
      6. Skill-term, Number of data points (e.g., courses) that have that skill-term, Number of jobs that have skill-term, Other information as needed
7. Create a visualization of the clusters in Tableau