from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool, SerperDevTool


class ResearchCrew:
    def __init__(self):
        self.researcher = Agent(
            role="연구원",
            goal="주제에 대한 철저한 연구 수행",
            backstory="당신은 주제에 대한 전문가로, 최신 정보를 찾아내고 이를 명확하게 전달하는 것을 잘합니다.",
            verbose=True,
            allow_delegation=False,
            tools=[SerperDevTool()],
            llm="openai/gpt-4o",
        )

        self.reporting_analyst = Agent(
            role="보고서 분석가",
            goal="{topic} 데이터 분석과 연구 결과를 바탕으로 상세 보고서 작성",
            backstory="당신은 세부사항에 대한 날카로운 통찰력을 가진 꼼꼼한 분석가입니다. 복잡한 데이터를 명확하고 간결한 보고서로 변환하여 다른 사람들이 쉽게 이해하고 활용할 수 있도록 만드는 능력으로 잘 알려져 있습니다.",
            verbose=True,
            allow_delegation=False,
            llm="openai/gpt-4o",
        )

        self.research = Task(
            description=(
                "1. {topic}에 대한 최신 뉴스 기사, 최신 유튜브 영상을 우선적으로 수집하세요.\n"
                "2. 수집한 뉴스 기사와 유튜브 영상을 정리하세요.\n"
                "3. 요약, 서론, 최신 뉴스 기사, 최신 유튜브 영상을 포함한 상세한 콘텐츠 개요를 연구하세요.\n"
                "4. 관련 데이터 또는 출처를 포함하세요."
            ),
            expected_output="개요, 독자 분석, SEO 키워드, 참고 자료가 포함된 종합적인 문서.",
            agent=self.researcher,
        )
        
        self.reporting = Task(
            description=(
                "1. 콘텐츠를 사용하여 매력적인 보고서를 작성하세요.\n"
                "2. 보고서는 관련된 모든 정보를 포함해야 하며 조사한 뉴스 기사와 유튜브 영상을 포함해야 합니다.\n"
                "3. 보고서는 최신 뉴스 기사와 유튜브 영상에 대한 간단한 요약을 포함해야합니다.\n"
                "4. 보고서가 요약, 서론, 최신 뉴스 기사, 최신 유튜브 영상으로 구성되어 있는지 확인합니다.\n"
                "5. 보고서는 한글로 작성됩니다.\n"
                "6. 출처는 콘텐츠의 실제 링크와 함께 작성됩니다.\n"
                "7. 보고서는 마크다운 형식으로 작성됩니다.\n"
                "8. 섹션/부제목은 매력적인 방식으로 적절하게 명명합니다.\n"
                "9. 문법적 오류를 검토하고 톤앤매너가 일치하는지 확인하세요.\n"
            ),
            expected_output="주요 주제들을 다루는 완성된 보고서로, 각 주제별로 상세한 정보 섹션을 포함합니다. '```' 없이 마크다운 형식으로 작성됩니다. 내용은 한글로 작성합니다.",
            agent=self.reporting_analyst,
            output_file="outputs/report.md",
        )

    def kickoff(self, *args):
        return Crew(
            agents=[self.researcher, self.reporting_analyst],
            tasks=[self.research, self.reporting],
            process=Process.sequential,
            verbose=True,
        ).kickoff(*args)
