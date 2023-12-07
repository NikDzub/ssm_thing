#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright
import os
import shutil
import json
import random
from pathlib import Path

cookies_json = os.listdir("./cookies_updated")


async def p1():
    async with async_playwright() as p:
        context = await p.firefox.launch(headless=False)
        page = await context.new_page(
            color_scheme="dark",
            # user_agent="Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36",
        )
        await context.contexts[0].add_cookies(
            json.loads(Path(f"cookies/coinitiktok.json").read_text())
            # json.loads(Path(f"cookies/bnadranfoensuragin.json").read_text())
        )

        block_media = ["image", "media", "font", "stylesheet"]
        await page.route(
            "**/*",
            lambda route: route.abort()
            if route.request.resource_type in block_media
            else route.continue_(),
        )

        await page.goto(
            "https://www.tiktok.com/@brentrivera/video/7309167673819303214",
            wait_until="load",
        )

        await page.wait_for_selector(
            'div[class*="DivCommentItemContainer"]', timeout=10000
        )

        eval_file = open("./interval.js", "r").read()

        try:
            for index, cookie in enumerate(cookies_json):
                try:
                    await page.evaluate(eval_file)
                    await page.wait_for_selector(".target", timeout=60000)

                    hearts_boxes = await page.query_selector_all(".heart_box")

                    hearts = await page.query_selector_all(".heart_box svg")

                    for heart in hearts:
                        if await heart.get_attribute("fill") == "currentColor":
                            print("is white")
                            await heart.click()
                            print("click")
                            await page.wait_for_timeout(2000)

                        # else:
                        #     print("is red")
                        #     await heart.click()
                        #     print("click")
                        #     await page.wait_for_timeout(2000)
                        #     await hearts_boxes[index].click()
                        #     print("click")

                    # await asyncio.gather(
                    #     *[
                    #         heart_handler(index, heart)
                    #         for index, heart in enumerate(hearts)
                    #     ]
                    # )
                    await context.contexts[0].add_cookies(
                        json.loads(Path(f"cookies_updated/{cookie}").read_text())
                    )
                    await page.wait_for_timeout(1000)
                    print(f"({index}/{len(cookies_json)}) {cookie}")
                    await page.reload(wait_until="load")

                except Exception as error:
                    print(error)
                    await context.contexts[0].add_cookies(
                        json.loads(Path(f"cookies_updated/{cookie}").read_text())
                    )
                    await page.wait_for_timeout(1000)
                    print(f"({index}/{len(cookies_json)}) {cookie}")
                    await page.reload(wait_until="load")
                    pass

        except Exception as error:
            print("comment not found")
            pass

        await page.wait_for_timeout(1000)
        await page.close()
        await context.close()


asyncio.run(p1())
