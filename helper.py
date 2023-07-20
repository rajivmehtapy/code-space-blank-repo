from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

def get_distance_info(prompt):
    messages = [
        SystemMessage(
            content="You are a helpful assistant."
        ),
        HumanMessage(
            content=prompt
        ),
    ]
    return chat(messages)

def get_row_details(prompt,llm):
    try:
        with open('gd.txt','w') as file:
            file.write(prompt)
        return [llm(prompt)]
    except Exception as ex:
        print(f'Error Occure -- {ex}')
        return [llm_openai(prompt)]

def convert_rows_to_list(info):
    for item in info:
        try:
            data = json.loads(item['rows'])
        except Exception as ex:
            data = item['rows'].split(',')   
        try:    
            type(data[0])
        except Exception as ex:
            data=[data]
        item['rows'] = data
    return info

def get_tool_wise_version_number(tool_id):
    sql=f"""
    select 
        row_number() OVER (ORDER BY number) AS row_no,
        number,
        tool_id,
        0 as tool_version_security_vulnerabilities,
        0 as tool_version_distance_from_latest_version
    from versions_data_df
    where tool_id = {tool_id}
    order by number
    """
    return sql_helper(sql)

def get_max_version_number(tool_id):
    sql=f"""
    select 
        row_number() OVER (ORDER BY number) AS row_no,
        number,
        tool_id,
        0 as tool_version_security_vulnerabilities,
        0 as tool_version_distance_from_latest_version
    from versions_data_df
    where tool_id = {tool_id}
    order by number desc
    """
    return sql_helper(sql)


def get_prompt(df,version_range,min_range,max_range):
    stuff = ''
    if len(min_range) != 0:
        stuff = f'''
                Can you give list of row_no from followings data whose number is within range of {min_range.replace('<','').replace('>','').replace('=','')} and {max_range.replace('>','').replace('<','').replace('=','')}
        row_no number
                '''.strip()
    else:
        stuff = f'''
                Can you give list of row_no from followings data whose number is equal {max_range.replace('>','').replace('<','').replace('=','')}
        row_no number
                '''.strip()
    for inx,row in df.iterrows():
        stuff += f'\n {row.row_no}, {row.number}'
    return stuff

def get_severity_predictions(prompt,tool_id,severity,llm):
    details = get_row_details(prompt,llm)
    print(f'detail is here {details}')
    rows = details
    predication={
        "tool_id":tool_id,
        "severity":severity,
        "rows": ','.join(rows)
    }
    return predication

def get_analytical_info_toolwise(analytical_info):
    rows=''
    for inx,item in enumerate(analytical_info):
        rows+=item['rows']+','
    
    tool_severity_info={
            'tool_id': analytical_info[0]['tool_id'], 
            'severity': analytical_info[0]['severity'], 
            'rows': list(set(rows[:-1].split(',')))
    }

    return tool_severity_info


def prepare_analytical_info(vulnerabilities_info_df,llm):
    analytical_info = []
    for inx,item in vulnerabilities_info_df.iterrows():
        min_range=''
        max_range=''
        version_range_list = json.loads(item.version_range)
        version_range = json.loads(item.version_range)[0].split(',')
        severity = item.severity
        tool_id = item.tool_id
        df = get_tool_wise_version_number(item.tool_id)
        for version_range_item in version_range_list:
            version_range = version_range_item.split(',')
            if len(version_range) == 1:
                max_range=version_range[0]
            else:
                min_range=version_range[0]
                max_range=version_range[1]
            prompt = get_prompt(df,version_range,min_range,max_range)
            print(prompt)
            analytical_info.append(get_severity_predictions(prompt,tool_id,severity,llm))
            max_range = ''
            min_range = '' 
            time.sleep(1)
    return analytical_info

def prepare_analytical_info_for_distance(vulnerabilities_info_df,llm):
    analytical_info = []
    for index,item in vulnerabilities_info_df.iterrows():
        tool_id = item.tool_id
        print(item.tool_id)
        df = get_tool_wise_version_number(item.tool_id)
        for inx,row in df.iterrows():
            latest_tool_version= get_max_version_number(tool_id)['number'][0]
            prompt = get_prompt_for_distance(current_tool_version=row.number,latest_tool_version=latest_tool_version)
            response = get_distance_info(prompt=prompt)
            print(response.content)
            information={
                'row_no':row.row_no,
                'tool_id':tool_id,
                'rank':response.content,
                'number':row.number,
            }
            analytical_info.append(information)
            time.sleep(1)
            if inx > 2:
                break
        break
    return analytical_info

def get_prompt_for_distance(current_tool_version,latest_tool_version):
    print(f'current_tool_version --> {current_tool_version}')
    template = f"""You are excellent AI assistant.You known to identify and quantize distance between two nodes.
    If we lable distance between in range of 1 - 5.
    that is if it's very near than label it as 1 and if it is too far
    it should label as 5. 
    For example

    if node1 is 1.0 and node2 is 2.0 than distance rank is 1.
    if node1 is 1.0 and node2 is 3.0 than distance rank is 2.
    if node1 is 1.0 and node2 is 4.0 than distance rank is 3.
    if node1 is 1.0 and node2 is 5.0 than distance rank is 4.
    if node1 is 5.0.0 and node2 is 5.2.0 than distance rank is 0.
    if node1 is 3.3.0 and node2 is 3.2.0 than distance rank is 0.
    if node1 is 4.4.0 and node2 is 5.2.0 than distance rank is 1.
    if node1 is 4.4.0-beta.8 and node2 is 5.5.0 than distance rank is 1.
    
    if node1 is 6.13.1 and node2 is 7.9.6 than distance rank is 1.
    if node1 is 6.14.0 and node2 is 7.9.6 than distance rank is 1.
    if node1 is 6.15.2 and node2 is 7.9.6 than distance rank is 1.
    if node1 is 6.21.0 and node2 is 7.9.6 than distance rank is 1.
    if node1 is 6.23.1 and node2 is 7.9.6 than distance rank is 1.
    if node1 is 6.3.1 and node2 is 7.9.6 than distance rank is 1.
    
    if node1 is 7.0.0-beta.54 and node2 is 7.9.6 than distance rank is 1.


        there is node1 is {current_tool_version} and node2 is {latest_tool_version}.

    now can you respond me what is the difference between node1 and node2 in terms of 
    rank between 1 to 5.
    Kindly give me response in one word only no need to verbose.
    Response:
    """
    return template

def convert_tool_version_External_Factors_Freshness_Distance_from_latest_version(response):
    print(f'Response --> {response}')
    internal_weitage=0
    rank=int(response)
    if rank >= 3 and rank <= 5:
        internal_weitage = 50
    elif rank >= 1 and rank <= 2: 
        internal_weitage = 90
    else:
        internal_weitage = 100

    return((internal_weitage/100)*5)   

def convert_tool_version_External_Factors_Freshness_Distance_from_latest_version(response):
    internal_weitage=0
    rank=int(response)
    if rank >= 3 and rank <= 5:
        internal_weitage = 50
    elif rank >= 1 and rank <= 2: 
        internal_weitage = 90
    else:
        internal_weitage = 100

    return((internal_weitage/100)*5)       