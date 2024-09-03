from crewai import Crew, Agent, Task
from openai import OpenAI
from langchain_ollama import ChatOllama

# Ollama와 연결된 LLM 생성
llm = ChatOllama(
    model="llama3.1",
    base_url="http://localhost:11434"
)

# Crew: 러닝 크루 => N명(조직)
# Agent: 요원 => 1명 (조직원)
# Task: 미션

# 쇼핑몰
# 요원의 역할, 목표, 역할 수행에 필요한 백스토리 등 세팅
book_agent = Agent(
    role='책 구매 어시스턴트',
    goal = '고객이 어떤 상황인지 설명을 하면 해당 사황에 맞는 우리 서점의 책을 소개합니다',
    backstory = '당신은 우리 서점의 모든 책 정보를 알고 있으며, 사람들의 상황에 맞는 책을 소개하는데 전문가입니다',
    llm = llm # LLM 모델 지정
) # 책 정보는 api로 내려줘야한다

# 사용자의 질문을 받아 지정할수도 있음
user_question = input('질문하시오: ')

# 요원마다 여러개의 타스크를 만들 수 있다
recommend_book_task = Task(
    # description='고객의 상황에 맞는 최고의 추천 도서 제안하기', # 미션 설명 
    description=user_question,
    expected_output='고객의 상황에 맞는 5개의 도서를 추천해주고, 해당 책을 추천한 이유를 알려줘',
    agent=book_agent, # 해당 미션을 수행할 에이전트를 지정
    output_file='recomend_task.md'
)


# 리뷰 분석 에이전트
# book 에이전트의 응답을 리뷰 에이전트에 던질 수 있다.
# 리뷰 에이전트는 추천받은 5개 책에 대해 task를 수행하고, 그 결과를 응답할 수 있다.
review_agent = Agent(
    role='책 리뷰 어시스턴트',
    goal = '추천 받은 책들의 도서에 대한 리뷰를 제공하고, 해당 도서에 대한 심도있는 평가를 제공합니다',
    backstory = '당신은 우리 서점의 모든 책 정보를 알고 있으며, 추천 받은 책에 대한 전문가 수준의 리뷰를 제공합니다',
    llm = llm # LLM 모델 지정
) 


review_task = Task(
    description='고객이 선택한 책에 대한 리뷰를 제공합니다',
    expected_output='고객이 선택한 책에 대한 리뷰를 제공합니다',
    agent=review_agent ,
     output_file='review_task.md'
)


# 요원과 미션을 관리
crew = Crew(
    agents=[book_agent, review_agent],
    tasks = [recommend_book_task,  review_task],
    verbose=True
)

result = crew.kickoff()
print(result)


# 우리가 하는 것
# 파이썬을 활용한 LLM - ollma, CrewAI
# 언어 모델 핸들링 -> 결과 값을 자바 서버에 전달 
# - REST API(Python-Framework) => 자바 서버

# Flask(쉬움, 진입 장벽 낮음) , FastAPI(진입장벽이 있는편)
# 1. 깃헙 스타
# 2. 구글 검색량
# -대부분의 AI기업들은 메인 서버를두고, AI 관련 인퍼런스(추론값) 값은 Python 백엔드로 내려주는 형태



