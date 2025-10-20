# 🎬 The Movie Database ETL

## 📘 Project Context and Goals
The project focuses on building an ETL pipeline to collect **currently airing movies** in Australia from the **The Movie Database API**.  
The pipeline continuously upserts new movies into a database, creating a growing and up-to-date table of films currently showing in Australian cinemas.

---

## 📊 Datasets Selected
- **TMDB API**: Provides daily updating data on currently airing movies in Australian cinemas, including release date, genre and popularity scores.  
- **Genres**: A .csv file mapping genre IDs to genre names.  
- **Language Codes**: A .csv file mapping language codes to languages. 

**Dataset Summary:**  
- 1 API endpoint (TMDB)  
- 2 CSV's

---

## 🏗️ Solution Architecture Diagram
Below is a simplified architecture diagram outlining the ETL workflow.   

![Solution Architecture](images/Solution%20Architecture.drawio.png)

---

## ⚙️ ETL Techniques Applied
1. **Extract:**  
   - Fetched movie data from the TMDB API in Python.
   - Used full extract as records have changing rating / popularity cores.   
   - Read supporting datasets (`genres.csv` and `language_codes.csv`) using `pandas`.  

2. **Transform:**  
   - Renaming columns
   - Joining/Merging data frames
   - Data type casting
   - Rounding
   - Exploding then group by

3. **Load:**  
   - Upsert: Append new movie releases and update already loaded movies ratings.  
   
---

## 📁 Final Dataset and Demo
   - docker run --env-file .env movie_etl:1.5

---

## 💡 Lessons Learnt
- API Pagination
- Importance of building clean **(modularised & functional/OOP)** code from the start 
- Don't do project 2 and 3 by myself 🙃

---
