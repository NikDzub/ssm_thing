#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright
import os
import shutil
import json
import random
from pathlib import Path

cookies_json = os.listdir("./cookies")


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
            'div[class*="DivLikeWrapper"] svg[fill="currentColor"]', timeout=10000
        )

        try:
            hearts = await page.query_selector_all(
                'div[class*="DivLikeWrapper"] svg[fill="currentColor"]'
            )

            for heart in hearts:
                await heart.click()
                await page.wait_for_timeout(500)
                print("click")
        except Exception as error:
            print(error)
            pass

        await page.wait_for_timeout(104354300)
        await page.close()
        await context.close()


asyncio.run(p1())
