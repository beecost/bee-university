import asyncio
import os
import time

import aiohttp as aiohttp
import requests

from config.config_university_project import ConfigUniversityProject
from helper.agent_helper import get_user_random_agent
from helper.array_helper import get_sublists
from helper.async_helper import multi_task_merge_results
from helper.error_helper import log_error
from helper.logger_helper import LoggerSimple
from helper.multithread_helper import multithread_helper
from helper.reader_helper import store_jsons_perline_in_file

logger = LoggerSimple(name=__name__).logger


def get_info(sbd):
    # url_api = 'https://diemthi.tuoitre.vn/search-thpt-score'
    # url_api = 'https://diemthi.tuoitre.vn/csv-thpt-score'
    url_api = f'https://dantri.com.vn/thpt/1/0/99/{sbd}/2023/0.2/search-gradle.htm'
    # body = {"data": sbd, "code": ""}
    data_exam = None

    try:
        # response = requests.post(url=url_api, data=body)
        response = requests.get(url=url_api)
        # logger.info(f'{sbd} - {response.text}')
        if response.status_code == 200:
            data = response.json()
            if data.get('student') and data.get('student').get('sbd') is not None:
                # result =
                # logger.info(response.text)
                data_exam = data.get('student')
                # logger.info(f"{sbd} - {data_exam.get('score')}")
    except Exception as e:
        log_error(e)
        logger.error(f'ERROR: sbd={sbd}')

    return data_exam


async def get_info_async(sbd):
    # url_api = 'https://diemthi.tuoitre.vn/search-lop10-score'
    # url_api = 'https://diemthi.tuoitre.vn/search-thpt-score'
    # url_api = 'https://diemthi.tuoitre.vn/csv-thpt-score'
    url_api = f'https://dantri.com.vn/thpt/1/0/99/{sbd}/2023/0.2/search-gradle.htm'
    body = {"data": sbd, "code": ""}
    data_exam = None
    header = {
        'user-agent': get_user_random_agent(),
        # 'cookie': 'G_ENABLED_IDPS=google; fpsend=149436; __zi=3000.SSZzejyD3CiaW_sbrKeErsE1gRkRH1QKFvEZf8a6188lrRBZnmC5ncNTjkp33K_1Ojp-xCSEJyPatFlg.1',
        # 'cookie': '_ttsid=cd90f0286ee983b48df479eed2a1a6cef2a347c00b22d719e59377b8437e5216',
        'cookie': 'uuid=72e1b7ed-17b1-4a50-b730-686522cc0801; menu_home_v2=menu_home_v2; title_newest_v2=title_newest_v2; title_article_lot_v2=title_article_lot_v2; _pk_id.6.0a2f=358b0b91d699c785.1684980667.; _ga=GA1.1.666941059.1642398522; _clck=c7dopm|2|fbw|0|1240; _cc_id=49d8f8e622b692da1207999694a54363; cto_bundle=AN9FG19EMVZBM2ZYYjhDcFhXJTJGUmpRJTJGY1kwbk9RS2JKb1lKcWlhd2NQb1REbFlnVEJYMU9rWXAwdldnZzFNaG1VUVFwMEpBJTJGRnB2SENFc1FFcjBSSHV5VDRKa1ZMUHdPJTJGUTl3cm96SldMNUxoJTJGM0JjTFB2OVVyQ2pWNkV4bVJkRmdQOU40aUVWYThjcTdTb3AwVUpFdnNqSElnJTNEJTNE; __gads=ID=7cb5f7c4d736d7b3:T=1684980668:S=ALNI_MbAiG6eymWQ6aGb5DCNr2pzSLeiLg; __gpi=UID=00000c0a533c9709:T=1684980668:RT=1684980668:S=ALNI_Matg-m18GW-U0485ifYGa8fCT8URQ; FCNEC=%5B%5B%22AKsRol90W6s7AODlJ7JK0o7fboor8ydh5ZZX0um1306FFtRA23I8tCegl69WbN7ljHvCr9wbvC3E1sSIOMCP7YEoV-OjSkEc40RxA6aASUxs78ch9Ymp3tFriFT8G3zOqC7Sn91CfzE0LDBfQiii-b6hUaIvgefccg%3D%3D%22%5D%2Cnull%2C%5B%5D%5D; _ga_E9JBQPRHRK=GS1.1.1684980667.1.1.1684980727.60.0.0; _ga_7SV2MJP43D=GS1.1.1684980668.1.1.1684980727.1.0.0; g_state={"i_p":1689517031489,"i_l":4}; menu_home_v3=menu_home_v3; .AspNetCore.Mvc.CookieTempDataProvider=CfDJ8Cc9GpixYQBGtnSGB6wzi1Ee7uh9AN1TJEPgMNQjucCUbx-4TeB5Atu-6g1yThWG05WLlAloOLGYRGyTUsZQo9BHIsvQWmG2MqYbHS5OA61m1ZAsT6E0cm49CdwrgSOAjOGLjnixxqlhuQrYwJr_m48Rc88HxkEVsNcEed5xTiyWnWL8Fu1Vr67wBqag_Ipsiw',
    }
    retry = 0
    max_retry = 3
    while data_exam is None and retry < max_retry:
        retry += 1
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                # async with session.post(url=url_api, headers=header, data=body, timeout=60) as res:
                async with session.get(url=url_api, headers=header, timeout=60) as res:
                    if res.status == 200:
                        response = await res.text()
                        # logger.info(f'{sbd} - {response}')
                        data = await res.json()
                        # logger.info(f'{data.get("data")}')
                        if data.get('student') and data.get('student').get('sbd') is not None:
                            # result =
                            # logger.info(response.text)
                            data_exam = data.get('student')
                            # logger.info(f"{sbd} - {data_exam}")
        except Exception as e:
            log_error(e)
            logger.error(f'retry={retry} - ERROR: sbd={sbd}')

    return data_exam


def build_sbd(provide_id, post_sbd):
    prefix = ''.join(['0' for i in range(6 - len(str(post_sbd)))])
    # logger.info(prefix)
    return f'{provide_id}{prefix}{post_sbd}'


def get_min_max_by_code(provide_id='64'):
    min = 1
    max = 999999

    sbd = max
    should_find = True
    mid = int((max - min) / 2) + min
    while should_find:
        if ((min - max) ** 2) == 1:
            # logger.info(f'find end sbd = {mid}')
            break
        mid = int((max - min) / 2) + min
        sbd = build_sbd(provide_id=provide_id, post_sbd=mid)
        logger.info(f'estimate sbd: {sbd}')
        result = get_info(sbd)
        if result is None:
            max = mid
            continue
        else:
            min = mid
            continue
        # max = int(max / 2)

        # info_obj = get_info(sbd)
    # logger.info(f'max = {max} min = {min}')
    return mid


async def job_crawler():
    # lst_provide = ['{0:02}'.format(num) for num in range(1, 65)]
    lst_provide = ['{0:02}'.format(num) for num in range(1, 65)]
    for provide_id in lst_provide:
        try:
            start_at = time.time()
            logger.info(f'prepare crawl provide: {provide_id}')

            # provide_id = 64
            batch_sbd = 5000

            max_sbd = get_min_max_by_code(provide_id)
            logger.info(f'max_sbd: {provide_id} - {max_sbd}')
            # max_sbd = 5743
            lst_sbd = []
            for pos in range(1, max_sbd):
                sbd = build_sbd(provide_id=provide_id, post_sbd=pos)
                lst_sbd.append(sbd)

            lst_task = []
            file_diemthi_path = ConfigUniversityProject().file_diemthi_path(provide_id=provide_id)
            for idx, _sbd in enumerate(lst_sbd):
                # if os.path.exists(file_diemthi_path):
                #     logger.info(f'skip: {file_diemthi_path}')
                #     continue
                # lst_obj_sbd = multithread_helper(items=sub_lst_sbd, method=get_info, timeout_concurrent_by_second=36000,
                #                                  max_workers=50, debug=False)

                lst_task.append(get_info_async(sbd=_sbd))
            lst_obj_sbd = await multi_task_merge_results(lst_task=lst_task, ignore_none=True,
                                                         concurrency=20)
            store_jsons_perline_in_file(jsons_obj=lst_obj_sbd, file_output_path=file_diemthi_path)
            logger.info(
                f'crawled provide_id={provide_id} students={len(lst_obj_sbd)} in {(time.time() - start_at) * 1000} ms -> {file_diemthi_path}')
        except Exception as e:
            logger.error(e)

    # get_info(sbd='02055358')


if __name__ == '__main__':
    # logger.info(get_info(sbd='01000016'))
    # job_crawler()
    asyncio.run(
        # get_info_async(sbd='01030725')
        job_crawler()
    )
    # logger.info(get_min_max_by_code(provide_id='01'))
