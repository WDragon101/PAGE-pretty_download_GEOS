# _*_ coding=utf-8 _*_
# created by Zhao Bailong
# Created on 2025-06-30
# Updated on 2025-07-01

import os
import argparse
import requests
import pandas as pd
from fake_useragent import UserAgent
from rich.progress import Progress
from rich.console import Console
from rich.pretty import pprint
from time import sleep
from datetime import datetime
from rich.live import Live
from rich.table import Table
from rich.align import Align
from rich.panel import Panel
from rich.progress import SpinnerColumn, TimeElapsedColumn, DownloadColumn


def init_log_console(log_file_name):
    with open(log_file_name, "wt") as log:
        console = Console(file=log)
        console.print(Panel(f"Pretty Appearance Good Experience\nCreated by Zhao Bailong\nEmail: [u "
                            f"blue]bailongzhao@163.com[/]",
                            title="Welcome PAGE!",
                            subtitle="Have A Nice Trip!"))


def log_renderable(log_file_name, renderable_object):
    with open(log_file_name, "a") as log:
        Console(file=log, width=129).log(renderable_object)


def initiate_setup_workspace():
    # setup workspace as script_dir
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    os.chdir(script_dir)
    return script_dir


def parse_input():
    # parse input from terminal
    parser = argparse.ArgumentParser(description='Download GEO files with Pretty Guide.')
    parser.add_argument('-i', '--input', required=True, help='such as "./GEOsources.txt"')
    args = parser.parse_args()
    return args


def parse_source(file_name):
    source_dic = {}
    with open(file_name, "r") as GS:
        for row in GS.readlines():
            source_fil = row.split()[0]
            source_url = row.split()[1]
            source_dic[source_fil] = source_url
    return source_dic


def check_remote_size(remote_link):
    session = requests.Session()
    try:
        res = session.get(url=remote_link, headers={"user-agent": UserAgent().random}, stream=True, timeout=300)
        if res.status_code == 200:
            size = int(res.headers.get('content-length', 0))
        else:
            size = 0
        return [res.status_code, size]
    except Exception as e:
        show_on_console.log(e)
        log_renderable(log_file, e)
        return ['error', 0]
    finally:
        session.close()


def check_local_size(file_name):
    file_exists = os.path.exists(file_name)
    file_size = os.path.getsize(file_name) if file_exists else 0
    return file_size


def generate_table():
    table = Table()
    for col in df.columns:
        if col == 'Remote Size' or col == 'Local Size':
            table.add_column(col, justify="right")
        else:
            table.add_column(col)
    for _, row in df.iterrows():
        if row['Status Code'] == 200 and row['Remote Size'] > 0 and row['Remote Size'] == row['Local Size']:
            table.add_row(f"[bold]{row['Index']}",
                          f"[b blue]{row['GEO file']}",
                          f"[i blue]{row['GEO link']}",
                          f"[i green]{row['Status Code']}",
                          f"[i green]{row['Remote Size']}",
                          f"[i green]{row['Local Size']}")
        else:
            table.add_row(f"[bold red]{row['Index']}",
                          f"[b blue]{row['GEO file']}",
                          f"[i blue]{row['GEO link']}",
                          f"[i red]{row['Status Code']}",
                          f"[i red]{row['Remote Size']}",
                          f"[i blue]{row['Local Size']}")
    return table


def task_table(dataframe):
    table = Table()
    for col in dataframe.columns:
        if col == 'Remote Size' or col == 'Local Size':
            table.add_column(col, justify="right")
        else:
            table.add_column(col)
    for _, row in dataframe.iterrows():
        table.add_row(f"[bold red]{row['Index']}",
                      f"[b blue]{row['GEO file']}",
                      f"[i blue]{row['GEO link']}",
                      f"[i red]{row['Status Code']}",
                      f"[i red]{row['Remote Size']}",
                      f"[i blue]{row['Local Size']}")
    return table


def denovo_download(output, source_url, remote_size):
    while True:
        try:
            res = requests.get(source_url, headers={"user-agent": UserAgent().random}, stream=True, timeout=300)
            with open(output, "wb") as file, tqdm(
                    desc=output,
                    total=remote_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024
            ) as bar:
                for data in res.iter_content(chunk_size=8192):
                    file.write(data)
                    bar.update(len(data))
            break
        except Exception as e:
            show_on_console.log(e)
            log_renderable(log_file, e)
            sleep(1)


if __name__ == "__main__":
    log_file = f"PAGE log {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.txt"
    init_log_console(log_file)

    show_on_console = Console()

    show_on_console.rule(f"[bold red]Welcoming! Pretty Appearance Good Experience!")
    log_renderable(log_file, f"[bold red]Welcoming! Pretty Appearance Good Experience!")

    workspace = initiate_setup_workspace()
    show_on_console.log(f"[bold blue]Present:[/] [bold i green]{workspace}")
    log_renderable(log_file, f"[bold blue]Present:[/] [bold i green]{workspace}")

    input_file = parse_input().input
    show_on_console.log(f"[blue]Sources:[/] [bold i green]{input_file}")
    log_renderable(log_file, f"[blue]Sources:[/] [bold i green]{input_file}")

    sources = parse_source(input_file)
    show_on_console.log(f"[blue]Summary:[/] [bold yellow]{len(sources)}[/] items")
    log_renderable(log_file, f"[blue]Summary:[/] [bold red]{len(sources)}[/] items")

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', None)
    df = pd.DataFrame(columns=["Index", "GEO file", "GEO link", "Status Code", "Remote Size", "Local Size"])
    index = 0
    with Live(generate_table(), refresh_per_second=4) as live:
        for key in sources.keys():
            index += 1
            init_info = {"Index": index,
                         "GEO file": key,
                         "GEO link": sources[key],
                         "Status Code": "",
                         "Remote Size": "",
                         "Local Size": ""}
            init_df = pd.DataFrame([init_info], index=[0])
            df = pd.concat([df, init_df], ignore_index=True)

            status, remote = check_remote_size(init_info["GEO link"])
            df.loc[df["GEO file"] == key, "Status Code"] = status
            df.loc[df["GEO file"] == key, "Remote Size"] = remote

            local = check_local_size(init_info["GEO file"])
            df.loc[df["GEO file"] == key, "Local Size"] = local
            live.update(generate_table())

    # overview dataframe
    # Index GEOFILE GEOLINK STATUSCODE REMOTESIZE LOCALSIZE
    log_renderable(log_file, f"Judge GEOs whether exist already")
    log_renderable(log_file, df)

    log_renderable(log_file, f"Create tasks downloading")
    local_none_geos = df[df['Local Size'] < df['Remote Size']]

    show_on_console.log(f"[blue]Tasks:[/] [bold yellow]{len(local_none_geos)}[/] geos")
    log_renderable(log_file, f"[blue]Tasks:[/] [bold yellow]{len(local_none_geos)}[/] geos")
    show_on_console.print(task_table(local_none_geos))

    with Progress(
            SpinnerColumn(),
            *Progress.get_default_columns(),
            TimeElapsedColumn(),
            DownloadColumn()
    ) as progress:
        log_renderable(log_file, "[red] Processing...")

        for _, row in local_none_geos.iterrows():
            while True:
                try:
                    log_renderable(log_file, f"[red] Downloading...{row['GEO file']} {row['GEO link']}")
                    res = requests.get(row['GEO link'], headers={"user-agent": UserAgent().random}, stream=True,
                                       timeout=300)
                    task = progress.add_task(f"[red]{row['GEO file']}", total=int(res.headers.get('content-length', 0)))
                    with open(row['GEO file'], "wb") as file:
                        for data in res.iter_content(chunk_size=8192):
                            file.write(data)
                            progress.update(task, advance=len(data))

                except Exception as e:
                    show_on_console.log(e)
                    log_renderable(log_file, e)
                    sleep(1)
                if os.path.getsize(row['GEO file']) == int(res.headers.get('content-length', 0)):
                    log_renderable(log_file, f"[red] Complete...{row['GEO file']}")
                    break
                else:
                    progress.update(task, completed=True)
                    continue
