#!/usr/bin/env python3


import asyncio
from playwright.async_api import async_playwright
import os
import shutil
import json
import random
from pathlib import Path


async def block_media(route, req):
    if req.resource_type in {"image", "media", "font", "stylesheet"}:
        try:
            await route.abort()
        except:
            pass


cookies_json = os.listdir("./cookies")


async def p1():
    async with async_playwright() as p:
        context = await p.firefox.launch(headless=False)
        # context.route("**/*", block_media)
        page = await context.new_page(color_scheme="dark")
        await page.goto(
            "https://www.tiktok.com/@rafaelaantico/video/7306962189225839877",
            wait_until="load",
        )
        await page.wait_for_timeout(1000)
        print("start")

        for cookie in cookies_json:
            try:
                await context.contexts[0].add_cookies(
                    json.loads(Path(f"cookies/{cookie}").read_text())
                )
                print(f"new cookie - {cookie}")
                await page.reload(wait_until="load")
                print("next user in 5sec")
                await page.wait_for_timeout(10000)

            except:
                pass

        await page.wait_for_timeout(1000)
        await page.close()
        await context.close()
        # await context.contexts[0].add_cookies(
        #     json.loads(Path("cookies/coinitiktok.json").read_text())
        # )
        # print("new cookie")
        # await page.wait_for_timeout(30053450)
        # await page.goto("https://www.tiktok.com", wait_until="load")
        # await page.wait_for_timeout(60000)


asyncio.run(p1())
