"""utility to generate mellow hyena reports"""

import sys

import calendar
import datetime
import jinja2

import pytz

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from typing import Dict, List

import yaml
from yaml.loader import SafeLoader

from postgres import PostGres
from sql_table import BoxScore


class DailyRow:
    """daily box score row"""

    adsb_hex_new = None
    adsb_hex_total = None
    device = None
    file_population = None
    score_date = None

    def __init__(self, args: BoxScore):
        self.adsb_hex_new = args.adsb_hex_new
        self.adsb_hex_total = args.adsb_hex_total
        self.device = args.device
        self.file_population = args.file_population
        self.score_date = args.score_date


class YearRow:
    """year row"""

    caption = None
    href = None

    def __init__(self, base_url: str, year: int):
        self.caption = str(year)
        self.href = f"{base_url}/{self.caption}.html"


class Reporter:
    """utility to create static HTML report"""

    base_url = None
    db_conn = None
    report_dir = None

    def __init__(self, base_url: str, report_dir: str, db_conn: str):
        self.base_url = base_url
        self.report_dir = report_dir
        self.db_conn = db_conn

    def get_years(self) -> List[int]:
        """return all known years"""

        years = []
        for ndx in range(2024, 2026):
            years.append(ndx)

        return years

    def write_year(self, environment: jinja2.environment.Environment, year: int):
        """write each daily box score for year"""

        db_engine = create_engine(self.db_conn, echo=False)
        postgres = PostGres(sessionmaker(bind=db_engine, expire_on_commit=False))

        range_limit = 366 if calendar.isleap(year) else 365
        new_years_day = datetime.date(year, 1, 1).toordinal()

        rows = []
        for ndx in range(range_limit):
            desired_ordinal = new_years_day + int(ndx)
            target_date = datetime.date.fromordinal(desired_ordinal)

            candidates = postgres.box_score_select_daily(target_date)
            if len(candidates) > 0:
                for row in candidates:
                    rows.append(DailyRow(row))

        template = environment.get_template("year.jinja")

        content = template.render(daily_list=rows, year=year)

        out_filename = f"{self.report_dir}/{year}.html"
        with open(out_filename, mode="w", encoding="utf-8") as message:
            message.write(content)

    def write_index(
        self, environment: jinja2.environment.Environment, years: List[int]
    ):
        """write index.html"""

        date_time_stamp = datetime.datetime.utcnow()
        formatted_date_time = date_time_stamp.strftime("%Y-%b-%d %H:%M:%S")

        rows = []
        for ndx in years:
            rows.append(YearRow(self.base_url, ndx))

        template = environment.get_template("index.jinja")

        content = template.render(report_date=formatted_date_time, year_list=rows)

        out_filename = f"{self.report_dir}/index.html"
        with open(out_filename, mode="w", encoding="utf-8") as message:
            message.write(content)

    def execute(self):
        """write report"""

        db_engine = create_engine(self.db_conn, echo=True)
        postgres = PostGres(sessionmaker(bind=db_engine, expire_on_commit=False))
        years = self.get_years()

        environment = jinja2.Environment(loader=jinja2.FileSystemLoader("."))

        self.write_index(environment, years)

        for ndx in years:
            self.write_year(environment, ndx)


print("start report")

#
# argv[1] = configuration filename
#
if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_name = sys.argv[1]
    else:
        config_name = "config.yaml"

    with open(config_name, "r", encoding="utf-8") as stream:
        try:
            configuration = yaml.load(stream, Loader=SafeLoader)
        except yaml.YAMLError as exc:
            print(exc)

    driver = Reporter(
        configuration["baseUrl"], configuration["reportDir"], configuration["dbConn"]
    )
    driver.execute()

print("stop report")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
