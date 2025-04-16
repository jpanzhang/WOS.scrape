from DrissionPage import ChromiumPage
import pandas as pd
import csv


df = pd.read_csv("keywords.csv")
f = open('output.csv', 'a', newline='')
writer = csv.DictWriter(f, fieldnames=["keyword_1", "keyword_2", "title", "date", "magzine_name"])
writer.writeheader()


for i in range(len(df)):
    keyword_1 = df.iloc[i, 0]
    keyword_2 = df.iloc[i, 1]

    page = ChromiumPage()
    page.get('https://webofscience.clarivate.cn/wos/alldb/basic-search')
    if page.ele('@class=onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon'):
        page.ele('@class=onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon').click()
        page.refresh()
    page.ele('@aria-label=Select search field Topic').click()
    page.ele('@title=Title').click()
    page.ele('text= Add row ').click()
    page.ele('@aria-label=Select search field Topic').click()
    page.ele('@title=Title').click()
    page.ele('@name=search-main-box').input(keyword_1)
    page.ele('@id=mat-input-1').input(keyword_2)
    page.ele('@data-ta=run-search').click()
    if page.ele('@class=onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon'):
        page.ele('@class=onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon').click()
    input("Please scroll smoothly to the bottom of the page and press Enter to continue.")
    print('done')
    # page.set.window.max()
    # page.set.scroll.smooth(on_off=True)
    # page.scroll.to_half()
    # page.scroll.to_bottom()
    # page.set.scroll.wait_complete()
    # page.refresh()

    if page.ele("@class=app-records-list"):

        records_lst = page.ele("@class=app-records-list")
        records = records_lst.eles( "tag=app-record")
        for record in records:
            title = record.ele("@data-ta=summary-record-title-link").text if record.ele("@data-ta=summary-record-title-link") else None
            date = record.ele("@name=pubdate").text if record.ele("@name=pubdate") else None
            magzine_name = record.ele(
                "@class=mat-focus-indicator mat-tooltip-trigger font-size-14 summary-source-title-link remove-space no-left-padding mat-button mat-button-base mat-primary ng-star-inserted").text if record.ele(
                "@class=mat-focus-indicator mat-tooltip-trigger font-size-14 summary-source-title-link remove-space no-left-padding mat-button mat-button-base mat-primary ng-star-inserted") else None
            dct_data = {
                "keyword_1": keyword_1,
                "keyword_2": keyword_2,
                "title": title,
                "date": date,
                "magzine_name": magzine_name
            }
            print(dct_data)
            # Result output
            writer.writerow(dct_data)
        else:

            page.clear_cache()
            page.refresh()
            continue

    page.clear_cache()
    page.refresh()
f.close()
