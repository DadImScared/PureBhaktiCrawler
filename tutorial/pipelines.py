# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import time

import models


class TutorialPipeline(object):
    def process_item(self, item, spider):
        print(spider.name)
        print("spider")
        print("\n")
        print("item")
        print(item)

        return item


class MoviePipeline(object):
    def process_item(self, item, spider):
        models.Movie.create_movie(**item)
        return item


class BookPipeline(object):
    """Saves items to Book database table"""
    def process_item(self, item, spider):
        """Return item"""
        models.Book.create_book(**item)
        return item


class HarmonistMagazinePipeline(object):
    """Saves items to HarmonistMagazine database table"""
    def process_item(self, item, spider):
        """Return item"""
        models.HarmonistMagazine.create_magazine(**item)
        return item


class BhagavatPatrikaPipeline(object):
    """Saves items to BhagavatPatrika database table"""
    def process_item(self, item, spider):
        """Return item"""
        clean_link = item['link'].rsplit('/', 1)[0].rsplit('/', 1)[1]
        # Extract year from link
        year = ''
        # Extract issue from link
        issue = ""

        issue_all = re.compile(r'issue-?[a-zA-z]+')
        multiple_issues = re.compile(r'issue-[0-9]+-?a?n?d?-?-[0-9]+')
        one_issue = re.compile(r'issue-[0-9]+$')
        year = re.search(r'year-[0-9]{4}', clean_link).group(0).strip().split('-')[-1]

        if issue_all.search(clean_link):
            issue = issue_all.search(clean_link).group(0).strip().split('-')
            issue = issue[-1]
            models.BhagavatPatrika.create_entry(**item, year=str(year), issue=str(issue))

        if multiple_issues.search(clean_link):
            issue = multiple_issues.search(clean_link).group(0).strip().split('-')
            issue = ",".join([x for x in issue if x.isdigit()]).split(',')
            print('issue \n')
            print(issue)
            models.BhagavatPatrika.create_entry(**item, year=str(year), issue=str(issue[0]))
            models.BhagavatPatrika.create_entry(**item, year=str(year), issue=str(issue[1]))

        if one_issue.search(clean_link):
            issue = one_issue.search(clean_link).group(0).strip().split('-')
            issue = issue[-1]
            models.BhagavatPatrika.create_entry(**item, year=str(year), issue=str(issue))
        return item




class HariKathaPipeline(object):
    """Saves items to HariKatha database table"""
    def process_item(self, item, spider):
        """Return item"""
        models.HariKatha.create_entry(**item)
        return item


class HarmonistMonthlyPipeline(object):
    """Saves items to HarmonistMonthly database table"""
    def process_item(self, item, spider):
        """Return item"""
        models.HarmonistMonthly.create_entry(**item)
        return item


class AudioLecturesPipeline(object):
    def process_item(self, item, spider):
        models.AudioLecture.create_entry(**item)
        return item


class BhajansPipeline(object):
    def process_item(self, item, spider):
        models.Song.create_entry(**item)
        return item