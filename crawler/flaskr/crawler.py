from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from .company_details import CompanyDetails


def crawl_for_business_by_name(businessName: str):
    with sync_playwright() as p:
        # Launch the search page
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://search.sunbiz.org/Inquiry/CorporationSearch/ByName")

        # Perform the search
        searchBar = page.get_by_label("Entity Name:")
        searchBar.fill(businessName)
        searchButton = page.get_by_role("button", name="Search Now")
        searchButton.click()

        # Ensure the results table is loaded
        page.wait_for_selector("#search-results table")  # Ensure the table is loaded

        # Extract the search results, parse the table and extract data
        table_html = page.query_selector("#search-results table").inner_html()
        soup = BeautifulSoup(table_html, "html.parser")
        rows = soup.find_all("tr")
        data = []

        # Process each row in the table
        for row in rows:
            columns = row.find_all("td")
            if len(columns) >= 3:  # Ensure there are enough columns
                # Extract the Corporate Name and Link
                link_tag = columns[0].find("a", href=True)
                corporate_name = link_tag.text.strip() if link_tag else None
                link = f"https://search.sunbiz.org{link_tag['href']}" if link_tag else None

                # Extract the Document Number and Status
                document_number = columns[1].text.strip()
                status = columns[2].text.strip()

                # Append the parsed data to the results list
                data.append({
                    "name": corporate_name,
                    "document_number": document_number,
                    "status": status,
                    "link": link
                })

        browser.close()

    return data

def parse_detail_sections(page):
    # Query all sections with the "detailSection" class
    detail_sections = page.query_selector_all(".detailSection")
    details = CompanyDetails()

    for section in detail_sections:
        section_text = section.text_content().strip()

        if "corporationName" in section.get_attribute("class"):
            # Handle corporationName section
            paragraphs = section.query_selector_all("p")
            if len(paragraphs) >= 2:
                details.corporation_type = paragraphs[0].inner_text().strip()
                details.entity_name = paragraphs[1].inner_text().strip()

        elif "filingInformation" in section.get_attribute("class"):
            # Handle filingInformation section
            labels = section.query_selector_all("label")
            values = section.query_selector_all("span:not(:has(label))")
            details.filing_information = {
                label.inner_text().strip(): value.inner_text().strip()
                for label, value in zip(labels, values)
            }

        elif "Principal Address" in section_text:
            # Handle Principal Address
            address_div = section.query_selector("div")
            if address_div:
                details.principal_address = address_div.inner_text().replace("\n", ", ").strip()

        elif "Mailing Address" in section_text:
            # Handle Mailing Address
            address_div = section.query_selector("div")
            if address_div:
                details.mailing_address = address_div.inner_text().replace("\n", ", ").strip()

        elif "Registered Agent" in section_text:
            # Handle Registered Agent
            agent_name = section.query_selector("span:not(:has(div))")
            agent_address_div = section.query_selector("div")
            if agent_name and agent_address_div:
                details.registered_agent = {
                    "name": agent_name.inner_text().strip(),
                    "address": agent_address_div.inner_text().replace("\n", ", ").strip(),
                }

        elif "Officer/Director Detail" in section_text:
            # Handle Officers and Directors
            title_spans = section.query_selector_all("span:has-text('Title')")
            for title_span in title_spans:
                # Extract the title
                title = title_span.text_content().strip()

                # Find the name element next to the title using JavaScript evaluation
                name = title_span.evaluate("""
                    el => {
                        const sibling = el.nextSibling;
                        return sibling && sibling.nodeType === Node.TEXT_NODE ? sibling.textContent.trim() : '';
                    }
                """)

                # Find the address within the same section
                address_div = title_span.query_selector("div")
                address = (
                    address_div.inner_text().replace("\n", ", ").strip()
                    if address_div
                    else ""
                )

                details.officers_directors.append(
                    {"title": title, "name": name, "address": address}
                )

    return details

def get_business_details(link: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(link)
        # Parse all detail sections
        detail_sections_data = parse_detail_sections(page)
        browser.close()
    return detail_sections_data