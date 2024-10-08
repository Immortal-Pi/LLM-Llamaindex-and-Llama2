import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()
# os.getenv('GROQ_API_KEY')
class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

        # self.llm = ChatGroq(
        # model_name='llama-3.1-70b-versatile',
        # temperature=0,
        # groq_api_key=os.getenv('GROQ_API_KEY'))

    def extract_jobs(self,cleaned_text):
        prompt_extract=PromptTemplate.from_template(
            """
                ### SCRAPED TEXT FROM WEBSITE:
                {page_data}
                ### INSTRUCTION:
                The scraped text is from the career's page of a website.
                Your job is to extract the job postings and return them in JSON format containing 
                following keys: 'role','experience','skills', 'description' and qualifications.
                Only returns the valid JSON.
                ### VALID JSON (NO PREAMBLE):
                """
        )
        chain_extract=prompt_extract|self.llm
        # print(chain_extract)
        res=chain_extract.invoke(input={'page_data':cleaned_text})

        try:
            json_parser=JsonOutputParser()
            res=json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException('Content too big, unable to parse jobs')
        return res if isinstance(res,list) else [res]

    def write_cover(self,job,links):
        prompt_letter=PromptTemplate.from_template(
            """
                ### JOB DESCRIPTION:
                {job_description}
    
                ###INSTRUCTION:
                You are Amruth, a Business Analyst doing his masters in Business Analytics and AI at University of Texas at Dallas. 
                You have exceptional skills in AI w.r.t deep learning, Machine Learning and LLM applications related projects.
Amruth is currently pursuing a Master of Science in Business Analytics & AI at the University of Texas at Dallas, building on their Bachelor’s degree in Computer Science and Engineering. With strong proficiency in Python, R, SQL, and AS400 (RPGLE/CLLE), they have hands-on experience with tools like VS Code, Tableau, Linux, and Hugging Face. Their machine learning expertise spans algorithms such as Random Forest, U-Net, and Logistic Regression, backed by certifications including IBM Professional Data Science and DeepLearning.AI TensorFlow Developer. 
During their tenure at Infosys as an Associate Consultant, they enhanced system performance by 15% through optimization and led the development of full-stack applications, including automating client reports via Java API integration with IBM-iSeries. They also mentored junior developers and ensured data consistency across platforms. In previous internships, they developed a Nike retail application using Java, Spring Boot, Angular, and MySQL, and contributed to a rural services mobile app with Google Maps API and Android Studio. 
Their projects include developing a satellite image segmentation model using U-Net and Hugging Face, and creating an IoT device for visually impaired individuals using YOLOv2, OpenCV, and text-to-speech APIs. Their blend of technical, analytical, and leadership skills positions them to make a significant impact in AI and data-driven roles.

                    Your job is to write a cover letter to the company regarding the job mentioned above describing the capability of Amruth 
                    in fulfilling their needs.
                    Also add the most relevant ones from the following links to showcase Amruth's portfolio: {link_list}
                    Remember you are Amruth, Masters student at University of Texas at Dallas. 
                    Do not provide a preamble.
                    ### COVER LETTER (NO PREAMBLE):
                """
        )
        chain_email= prompt_letter | self.llm
        res=chain_email.invoke({'job_description':str(job),'link_list':links})
        return res.content

if __name__ =='__main__':
    print(os.getenv("GROQ_API_KEY"))