import pandas as pd
import requests

# Replace with your actual Serper API key
SERPER_API_KEY = "" # Give api key of Scrpper Here
EXCLUDED_DOMAINS = {
    "spotify.com", "imdb.com", "tracxn.com", "amazon.com", "wikipedia.org",
    "linkedin.com", "facebook.com", "google.com", "findthecompany.com",
    "twitter.com", "instagram.com", "tiktok.com", "crunchbase.com",
    "i-d.vice.com", "open.spotify.com", "netflix.com", "vocabulary.com",
    "dictionary.com", "uscis.gov", "youtube.com", "apollo.io", "justdial.com",
    "upwork.com", "zaubacorp.com", "economictimes.indiatimes.com",
    "bloomberg.com", "iaccess.dnb.co.in", "glassdoor.co.in",
    "thecompanycheck.com", "vccircle.com", "dictionary.cambridge.org",
    "merriam-webster.com", "wellfound.com", "amazon.in", "signalhire.com",
    "yourstory.com", "in.indeed.com", "naukri.com", "business-standard.com",
    "ycombinator.com", "ambitionbox.com", "thesaurus.com", "en.wiktionary.org",
    "tofler.in", "indiamart.com", "britannica.com", "exchange4media.com",
    "m.economictimes.com", "connect2india.com", "dnb.com", "cleartax.in",
    "apps.apple.com", "digestivehealthinstitute.org", "easyleadz.com",
    "oxfordlearnersdictionaries.com", "knowyourgst.com",
    "find-and-update.company-information.service.gov.uk", "zoominfo.com",
    "pinterest.com", "in.pinterest.com", "flipkart.com", "tradeindia.com",
    "6sense.com", "companydetails.in", "falconebiz.com", "moneycontrol.com",
    "quickcompany.in", "softwaresuggest.com", "pin-code.org.in", "clutch.co",
    "insiderbiz.in", "indiafilings.com", "careers.smartrecruiters.com",
    "99corporates.com", "datanyze.com", "startupcaservices.com", "infopark.in",
    "lusha.com", "finance.yahoo.com", "rocketreach.co", "lawyerservices.in",
    "instafinancials.com", "vakilsearch.com", "leadzen.ai", "startupgali.com",
    "neverbounce.com", "mastersindia.co", "info.edgeinsights.in", "github.com",
    "reddit.com", "search.sunbiz.org", "zensuggest.com", "in.kompass.com",
    "indialei.in", "indiankanoon.org", "investopedia.com", "addresses.company",
    "bharatibiz.com", "tripadvisor.com", "glassdoor.com", "yelp.com",
    "safer.fmcsa.dot.gov", "homeadvisor.com", "opencorporates.com", "bbb.org",
    "mapquest.com", "tripadvisor.in", "yellowpages.com", "indeed.com",
    "groww.in", "internshala.com", "f6s.com", "techcrunch.com", "techymojo.in",
    "clodura.ai", "sulekha.com", "foundit.in", "indianyellowpages.net.in",
    "dhanvijay.in", "ynos.in", "hirist.tech", "planetexim.net", "iimjobs.com",
    "filesure.in", "cutshort.io", "placementindia.com", "expertia.ai",
    "jobhai.com", "shine.com", "instahyre.com", "emkayglobal.com",
    "pitchbook.com"
}

def get_domain(company_name):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"q": company_name}
    
    try:
        res = requests.post(url, headers=headers, json=payload)
        res.raise_for_status()
        data = res.json()
        for result in data.get("organic", []):
            link = result.get("link", "")
            if link:
                domain = link.split("/")[2]
                if domain not in EXCLUDED_DOMAINS:
                    return domain
    except Exception as e:
        print(f"Error fetching domain for {company_name}: {e}")
    return None

def fill_domains_from_csv(input_csv):
    df = pd.read_csv(input_csv)
    if 'Domain' not in df.columns:
        df['Domain'] = ""

    for index, row in df.iterrows():
        company = row['Company']
        if pd.isna(row['Domain']) or row['Domain'].strip() == "":
            print(f"Searching domain for: {company}")
            domain = get_domain(company)
            if domain:
                df.at[index, 'Domain'] = domain
                print(f" → Found: {domain}")
            else:
                print(" → No domain found.")
    
    df.to_csv("output_with_domains.csv", index=False)
    print("✅ Done! Updated file saved as 'output_with_domains.csv'.")

# Example usage
if __name__ == "__main__":
    fill_domains_from_csv(r"C:\Users\SAYAN\Desktop\Yourdost.csv")  # Change to your actual CSV filename
