import streamlit as st
from src.helper import extract_text_from_pdf,ask_openai
from src.job_api import fetch_likedin_jobs,fetch_naukri_jobs


st.set_page_config(page_title="Job Recommender",layout="wide")
st.title("AI Job Recommender")
st.markdown("Upload your resume and get job recommendations based on your skills and experience from LinkedIn and Naukri")

uploaded_file = st.file_uploader("Upload your resume(PDF)",type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        
    with st.spinner("Summarizing your resume..."):
        summary = ask_openai(f"summarize this resume highlighting the skills,education and experience:\n\n{resume_text}",max_tokens=400)
        
    with st.spinner("Finding skill Gaps..."):
        gaps = ask_openai(f"Analyze this resume and highlight missing skills,certification and experiences needed for better oppurtunities:\n\n{resume_text}",max_tokens=300)
        
    with st.spinner("Creating Future Roadmap..."):
        roadmap = ask_openai(f"Based on this resume suggest a future roadmap to improve this person's career prospects(skills to learn,certification needed, industry exposure):\n\n{resume_text}",max_tokens=200)
        
    # Display nicely formatted results
    st.markdown("---")
    st.header("📑 Resume Summary")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{summary}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🛠️ Skill Gaps & Missing Areas")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{gaps}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🚀 Future Roadmap & Preparation Strategy")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{roadmap}</div>", unsafe_allow_html=True)

    st.success("✅ Analysis Completed Successfully!")
    
    if st.button("Get Job Recommendations"):
        with st.spinner("Fetching Job Recommendations"):
            keywords = ask_openai(f"Based on this resume summary, suggest the best job titles and keywords for searching jobs. Give a comma-seperated list only, no explanation.\n\nSummary:{summary}",max_tokens=50)
            
            search_keywords_clean = keywords.replace("\n ","").strip()
            
        st.success(f"Extracted Job Keywords: {search_keywords_clean}")
        
        with st.spinner("Fetching Jobs from LinkedIn and Naukri"):
            linkedin_jobs = fetch_likedin_jobs(search_keywords_clean,rows=30)
            naukri_jobs = fetch_naukri_jobs(search_keywords_clean,rows=30)
            
        st.markdown("--------")
        st.header("Top LinkedIn Jobs (Inida)")
        if linkedin_jobs:
            for job in linkedin_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- {job.get('location')}")
                st.markdown(f" [View Job]({job.get('link')})")
                st.markdown("--------")
                
        else:
            st.warning("No LinkedIn jobs found")
            
        
        st.markdown("--------")
        st.header("Top Naukri Jobs (Inida)")
        if naukri_jobs:
            for job in naukri_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- {job.get('location')}")
                st.markdown(f" [View Job]({job.get('url')})")
                st.markdown("--------")
        
        else:
            st.warning("No Naukri jobs found")