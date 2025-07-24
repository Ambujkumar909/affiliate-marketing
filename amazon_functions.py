import time


async def Electronics(page, total_count, product_count, count):
    await page.select_option("select#searchDropdownBox", value="search-alias=electronics")
    await page.wait_for_timeout(3000)
    await page.click("#nav-search-submit-button")
    await page.wait_for_timeout(3000)
    # await page.click("a.nav-a.nav-hasArrow >> text=Mobiles & Accessories")
    # await page.wait_for_timeout(3000)
    # await page.click("a.a-link-normal >> text=10% Off or more")
    # await page.wait_for_timeout(3000)
    # mobile = ["Mobile Accessories"]  # , "Smartphones & Basic Mobiles", "Smartwatches"]
    # for x in mobile:
    #     await page.click(f"a.a-link-normal >> text={x}")
    #     await page.wait_for_timeout(3000)
    #     if x == "Smartphones & Basic Mobiles":
    #         await page.click('a.a-link-normal >> text=Smartphones')
    #         await page.wait_for_timeout(3000)
    #     for _ in range(1):
    #         await page.wait_for_selector('div[role="listitem"]', timeout=4000)

    #     # Get all product containers
    #         product_divs = await page.query_selector_all('div[role="listitem"]')

    #         print(f"Found {len(product_divs)} products on this page\n")
    #         total_count += len(product_divs)
    #         for product in product_divs:
    #             # Product Title
    #             title_elem = await product.query_selector("h2 span")
    #             title = await title_elem.inner_text() if title_elem else "N/A"

    #             # Product Link
    #             link_element = await product.query_selector('div[data-cy="title-recipe"] a')
    #             href = await link_element.get_attribute('href')
    #             if href and not href.startswith("javascript"):
    #                 product_url = f"https://www.amazon.in{href}"
    #             else:
    #                 count += 1
    #                 continue
    #             # Image URL
    #             img_elem = await product.query_selector("img")
    #             image_url = await img_elem.get_attribute("src") if img_elem else "N/A"

    #             # Price
    #             price_spans = await product.query_selector_all("span.a-offscreen")
    #             discounted_price = await price_spans[0].inner_text() if len(price_spans) > 0 else "N/A"
    #             original_price = await price_spans[1].inner_text() if len(price_spans) > 1 else "N/A"

    #             # Discount (optional)

    #             # Print product details
    #             print("Title:", title)
    #             print("Link:", product_url)
    #             print("Image URL:", image_url)
    #             print("Price:", discounted_price)
    #             print("original price:", original_price)
    #             print("-" * 80)
    #             time.sleep(0.08)
    #             product_count += 1
    #         await page.wait_for_timeout(3000)
    #         await page.click("a.s-pagination-next")
    #         await page.wait_for_timeout(3000)
    #     print("count\n", count)
    #     print("total_count\n", total_count)
    #     print("product_count\n", product_count)
    #     await page.locator("li.a-spacing-micro a").filter(has_text="Mobiles & Accessories").click()
    #     await page.wait_for_timeout(3000)
    count = 0
    total_count = 0
    product_count = 0
    await page.click("a.nav-a.nav-hasArrow >> text=Laptops & Accessories")
    await page.wait_for_timeout(3000)
    await page.click("a.a-link-normal >> text=10% Off or more")
    await page.wait_for_timeout(3000)
   
    Laptop = ['Accessories & Peripherals', 'Desktops', 'Monitors' , 'Tablets']
    for lp in Laptop:
        await page.locator("li.a-spacing-micro a").filter(has_text=lp).first.click()
        await page.wait_for_timeout(3000)
        if lp == "Printers, Inks & Accessories":
            await page.click('a.a-link-normal >> text=Printers')
            await page.wait_for_timeout(3000)
        for _ in range(1):
            await page.wait_for_selector('div[role="listitem"]', timeout=4000)

        # Get all product containers
            product_divs = await page.query_selector_all('div[role="listitem"]')

            print(f"Found {len(product_divs)} products on this page\n")
            total_count += len(product_divs)
            for product in product_divs:
                # Product Title
                title_elem = await product.query_selector("h2 span")
                title = await title_elem.inner_text() if title_elem else "N/A"

                # Product Link
                link_element = await product.query_selector('div[data-cy="title-recipe"] a')
                if not link_element:
                    count += 1
                    continue
                href = await link_element.get_attribute('href')
                if href and not href.startswith("javascript"):
                    product_url = f"https://www.amazon.in{href}"
                else:
                    count += 1
                    continue
                # Image URL
                img_elem = await product.query_selector("img")
                image_url = await img_elem.get_attribute("src") if img_elem else "N/A"

                # Price
                price_spans = await product.query_selector_all("span.a-offscreen")
                discounted_price = await price_spans[0].inner_text() if len(price_spans) > 0 else "N/A"
                original_price = await price_spans[1].inner_text() if len(price_spans) > 1 else "N/A"

                # Discount (optional)

                # Print product details
                print("Title:", title)
                print("Link:", product_url)
                print("Image URL:", image_url)
                print("Price:", discounted_price)
                print("original price:", original_price)
                print("-" * 80)
                time.sleep(0.08)
                product_count += 1
            await page.wait_for_timeout(3000)
            await page.click("a.s-pagination-next")
            await page.wait_for_timeout(3000)
        print("count\n", count)
        print("total_count\n", total_count)
        print("product_count\n", product_count)
        await page.locator("li.a-spacing-micro a").filter(has_text="Computers & Accessories").click()
        await page.wait_for_timeout(3000)
    await page.click("a.nav-a.nav-hasArrow >> text=TV & Home Entertainment")
    await page.wait_for_timeout(3000)
    await page.click("a.a-link-normal >> text=10% Off or more")
    await page.wait_for_timeout(3000)
    Televisions = ['Televisions']
    for tv in Televisions:
        await page.locator("li.a-spacing-micro a").filter(has_text=tv).first.click()
        await page.wait_for_timeout(3000)
        for _ in range(1):
            await page.wait_for_selector('div[role="listitem"]', timeout=4000)

        # Get all product containers
            product_divs = await page.query_selector_all('div[role="listitem"]')

            print(f"Found {len(product_divs)} products on this page\n")
            total_count += len(product_divs)
            for product in product_divs:
                # Product Title
                title_elem = await product.query_selector("h2 span")
                title = await title_elem.inner_text() if title_elem else "N/A"

                # Product Link
                link_element = await product.query_selector('div[data-cy="title-recipe"] a')
                if not link_element:
                    count += 1
                    continue
                href = await link_element.get_attribute('href')
                if href and not href.startswith("javascript"):
                    product_url = f"https://www.amazon.in{href}"
                else:
                    count += 1
                    continue
                # Image URL
                img_elem = await product.query_selector("img")
                image_url = await img_elem.get_attribute("src") if img_elem else "N/A"

                # Price
                price_spans = await product.query_selector_all("span.a-offscreen")
                discounted_price = await price_spans[0].inner_text() if len(price_spans) > 0 else "N/A"
                original_price = await price_spans[1].inner_text() if len(price_spans) > 1 else "N/A"

                # Discount (optional)

                # Print product details
                print("Title:", title)
                print("Link:", product_url)
                print("Image URL:", image_url)
                print("Price:", discounted_price)
                print("original price:", original_price)
                print("-" * 80)
                time.sleep(0.08)
                product_count += 1
            await page.wait_for_timeout(3000)
            await page.click("a.s-pagination-next")
            await page.wait_for_timeout(3000)
        print("count\n", count)
        print("total_count\n", total_count)
        print("product_count\n", product_count)
    await page.click("a.nav-a.nav-hasArrow >> text=Audio")
    await page.wait_for_timeout(3000)
    await page.click("a.a-link-normal >> text=10% Off or more")
    await page.wait_for_timeout(3000)
    await page.locator("li.a-spacing-micro a").filter(has_text='Speakers').first.click()
    speaker = ['Bluetooth Speakers', 'Home Theater Systems']
    for sp in speaker:
        await page.locator("li.a-spacing-micro a").filter(has_text=sp).first.click()
        await page.wait_for_timeout(3000)
        for _ in range(1):
            await page.wait_for_selector('div[role="listitem"]', timeout=4000)

        # Get all product containers
            product_divs = await page.query_selector_all('div[role="listitem"]')

            print(f"Found {len(product_divs)} products on this page\n")
            total_count += len(product_divs)
            for product in product_divs:
                # Product Title
                title_elem = await product.query_selector("h2 span")
                title = await title_elem.inner_text() if title_elem else "N/A"

                # Product Link
                link_element = await product.query_selector('div[data-cy="title-recipe"] a')
                if not link_element:
                    count += 1
                    continue
                href = await link_element.get_attribute('href')
                if href and not href.startswith("javascript"):
                    product_url = f"https://www.amazon.in{href}"
                else:
                    count += 1
                    continue
                # Image URL
                img_elem = await product.query_selector("img")
                image_url = await img_elem.get_attribute("src") if img_elem else "N/A"

                # Price
                price_spans = await product.query_selector_all("span.a-offscreen")
                discounted_price = await price_spans[0].inner_text() if len(price_spans) > 0 else "N/A"
                original_price = await price_spans[1].inner_text() if len(price_spans) > 1 else "N/A"

                # Discount (optional)

                # Print product details
                print("Title:", title)
                print("Link:", product_url)
                print("Image URL:", image_url)
                print("Price:", discounted_price)
                print("original price:", original_price)
                print("-" * 80)
                time.sleep(0.08)
                product_count += 1
            await page.wait_for_timeout(3000)
            await page.click("a.s-pagination-next")
            await page.wait_for_timeout(3000)
        print("count\n", count)
        print("total_count\n", total_count)
        print("product_count\n", product_count)
