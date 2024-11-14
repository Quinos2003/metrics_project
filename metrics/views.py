from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import re
import openpyxl
from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
import openpyxl
import re
from datetime import datetime
import chromedriver_autoinstaller as cda
from django.shortcuts import render
import os
import matplotlib.pyplot as plt
import io
import base64
def home(request):
    return render(request, 'home.html')
# def webpage_metrics(request):
#     if request.method == "POST":
#         url = request.POST.get('url')
#         try:
#             response = requests.get(url)
#             soup = BeautifulSoup(response.text, "html.parser")

#             # Calculate the metrics
#             links = len(soup.find_all('a', href=True)) + len(soup.find_all('link', href=True))
#             body_words = len(soup.find("body").text.split())
#             lists = len(soup.find_all("ol")) + len(soup.find_all("ul"))
#             tables = len(soup.find_all("table"))
#             title_length = len(soup.find("title").text)
#             page_size = 100 * body_words
#             graphics = len(soup.find_all("img")) + len(soup.find_all("svg")) + len(soup.find_all("canvas"))
#             text_emphasis = len(soup.find_all("b")) + len(soup.find_all("strong")) + len(soup.find_all("i")) + \
#                             len(soup.find_all("em")) + len(soup.find_all("u")) + len(soup.find_all("del")) + \
#                             len(soup.find_all("s")) + len(soup.find_all("sub"))
#             number_of_exclam = soup.find("body").text.count("!")
#             script_tag = len(soup.find_all("script"))
#             embedded_links = len(soup.find_all('a', href=True))
#             redirecting_links = len(soup.find_all('a', href=True))  # Simulating same value as embedded links
#             in_page_link = int(len(soup.find_all('link', href=True)) / 10)
#             frame_tags = len(soup.find_all("frame"))
#             total_number_of_words = len(soup.text.split())
#             meta_tags = len(soup.find_all("meta"))

#             # Create a metrics dictionary
#             metrics = {
#                 'number_of_link': links,
#                 'body_text_words': body_words,
#                 'number_of_list': lists,
#                 'number_of_tables': tables,
#                 'title_length': title_length,
#                 'page_size': page_size,
#                 'graphics': graphics,
#                 'text_emphasis': text_emphasis,
#                 'number_of_exclam': number_of_exclam,
#                 'number_of_script': script_tag,
#                 'embedded_links': embedded_links,
#                 'redirecting_links': redirecting_links,
#                 'in_page_link': in_page_link,
#                 'frames': frame_tags,
#                 'number_of_words': total_number_of_words,
#                 'number_of_meta_tags': meta_tags,
#             }

#             return render(request, 'metrics.html', {'metrics': metrics, 'url': url})

#         except Exception as e:
#             return HttpResponse(f"Error: {e}")

#     return render(request, 'metric_input_form.html')

def webpage_metrics(request):
    if request.method == "POST":
        url = request.POST.get('url')
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Calculate the metrics
            links = len(soup.find_all('a', href=True)) + len(soup.find_all('link', href=True))
            body_words = len(soup.find("body").text.split())
            lists = len(soup.find_all("ol")) + len(soup.find_all("ul"))
            tables = len(soup.find_all("table"))
            title_length = len(soup.find("title").text)
            page_size = 100 * body_words  # This is an approximation
            graphics = len(soup.find_all("img")) + len(soup.find_all("svg")) + len(soup.find_all("canvas"))
            text_emphasis = len(soup.find_all("b")) + len(soup.find_all("strong")) + len(soup.find_all("i")) + \
                            len(soup.find_all("em")) + len(soup.find_all("u")) + len(soup.find_all("del")) + \
                            len(soup.find_all("s")) + len(soup.find_all("sub"))
            number_of_exclam = soup.find("body").text.count("!")
            script_tag = len(soup.find_all("script"))
            embedded_links = len(soup.find_all('a', href=True))
            redirecting_links = len(soup.find_all('a', href=True))
            in_page_link = int(len(soup.find_all('link', href=True)) / 10)
            frame_tags = len(soup.find_all("frame"))
            total_number_of_words = len(soup.text.split())
            meta_tags = len(soup.find_all("meta"))

            # Helper function for categorization
            def categorize(value, mean, std):
                if value <= mean - std:
                    return "good", "green"
                elif value <= mean + std:
                    return "ok", "yellow"
                else:
                    return "worse", "red"

            # Define means and std for each metric
            metrics_data = {
                'number_of_link': (links, 112.85, 105.95),
                'body_text_words': (body_words, 7378.09, 8582.61),
                'number_of_list': (lists, 8.96, 11.32),
                'number_of_tables': (tables, 0, 0),
                'title_length': (title_length, 31.49, 26.20),
                'page_size': (page_size, 737809, 858260.93),
                'graphics': (graphics, 40.59, 48.03),
                'text_emphasis': (text_emphasis, 3.28, 9.63),
                'number_of_exclam': (number_of_exclam, 0.5, 1.17),
                'number_of_script': (script_tag, 29.43, 138.45),
                'embedded_links': (embedded_links, 73.92, 71.09),
                'redirecting_links': (redirecting_links, 73.92, 71.09),
                'in_page_link': (in_page_link, 3.47, 5.18),
                'frames': (frame_tags, 0, 0),
                'number_of_words': (total_number_of_words, 7436.95, 8588.48),
                'number_of_meta_tags': (meta_tags, 18.24, 11.54)
            }

            # Create categorized metrics dictionary
            metrics = {}
            for key, (value, mean, std) in metrics_data.items():
                category, color = categorize(value, mean, std)
                metrics[key] = {
                    "value": value,
                    "category": category,
                    "color": color
                }

            # Render the results in the template
            return render(request, 'metrics.html', {'metrics': metrics, 'url': url})

        except Exception as e:
            return HttpResponse(f"Error: {e}")

    return render(request, 'metric_input_form.html')

def analyze_metrics(request):
    if request.method == "POST":
        # Ensure Chrome driver is installed automatically
        cda.install()

        # Set user-agent and configure Chrome options
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')

        # Get the single URL from the form input
        url = request.POST.get('url')  # Assuming the form has a single URL input field

        if not url:
            return HttpResponse("No URL provided.", status=400)

        # Initialize list to hold metrics data
        metrics_data = []

        start = time.time()

        # Initialize the WebDriver and open the measurement site
        driver = webdriver.Chrome(options=options)
        driver.get("https://web.dev/measure/")

        # Input the URL and click Analyze
        text_field = driver.find_element(By.NAME, "url")
        text_field.send_keys(url)
        button = driver.find_element(By.XPATH, "//button[span[text()='Analyze']]")
        button.click()

        # Wait for metrics to load
        time.sleep(15)

        # Extract the performance metrics from the page
        metric_elements = driver.find_elements(By.CSS_SELECTOR, ".OyzgL")
        lcp_value = inp_value = cls_value = fcp_value = ttfb_value = None

        for element in metric_elements:
            metric_text = element.text
            if "Largest Contentful Paint (LCP)" in metric_text:
                lcp_value = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", metric_text)[0])
            if "Interaction to Next Paint (INP)" in metric_text:
                inp_value = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", metric_text)[1])
            if "Cumulative Layout Shift (CLS)" in metric_text:
                cls_value = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", metric_text)[2])
            if "First Contentful Paint (FCP)" in metric_text:
                fcp_value = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", metric_text)[3])
            if "Time to First Byte (TTFB)" in metric_text:
                ttfb_value = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", metric_text)[4])

        # Thresholds for each metric
        thresholds = {
            "lcp": {"min": 1.7, "max": 19.4, "mean_median_max": 3.9},
            "inp": {"min": 30, "max": 498, "mean_median_max": 138},
            "cls": {"min": 0, "max": 5.4, "mean_median_max": 0.065},
            "fcp": {"min": 1.4, "max": 3, "mean_median_max": 2.65},
            "ttfb": {"min": 0.5, "max": 1.9, "mean_median_max": 1.55},
        }

        # Categorize each metric based on thresholds
        def categorize(value, metric):
            if value <= thresholds[metric]["mean_median_max"]:
                return "GOOD"
            elif value <= thresholds[metric]["max"]:
                return "OK"
            else:
                return "WORSE"

        lcp_category = categorize(lcp_value or 4.1, "lcp")
        inp_category = categorize(inp_value or 30, "inp")
        cls_category = categorize(cls_value or 5.4, "cls")
        fcp_category = categorize(fcp_value or 3.0, "fcp")
        ttfb_category = categorize(ttfb_value or 1.9, "ttfb")

        # Store metrics and categories in a list
        metrics_data.append({
            "url": url,
            "lcp": {"value": lcp_value, "category": lcp_category},
            "inp": {"value": inp_value, "category": inp_category},
            "cls": {"value": cls_value, "category": cls_category},
            "fcp": {"value": fcp_value, "category": fcp_category},
            "ttfb": {"value": ttfb_value, "category": ttfb_category},
        })

        # Close the driver after extracting the data
        driver.quit()

        # Log the time taken for the process
        end = time.time()
        taken_time = datetime.utcfromtimestamp(end - start)
        taken_time_str = f"{taken_time.minute} Min(s) " if taken_time.minute > 0 else ""
        taken_time_str += f"{taken_time.second} Sec(s)" if taken_time.second > 0 else "0.0 Sec(s)"
        print(f"Success \nTime Taken :- {taken_time_str}")
        return render(request, "metric_result.html", {"metrics_data": metrics_data})

    return render(request, "metric_input_form.html")




# def analyze_metrics(request):
#     if request.method == "POST":
#         # Ensure Chrome driver is installed automatically
#         cda.install()

#         # Configure Chrome options
#         user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
#         options = webdriver.ChromeOptions()
#         options.headless = True
#         options.add_argument(f'user-agent={user_agent}')
#         options.add_argument("--window-size=1920,1080")
#         options.add_argument('--ignore-certificate-errors')
#         options.add_argument('--allow-running-insecure-content')
#         options.add_argument("--disable-extensions")
#         options.add_argument("--proxy-server='direct://'")
#         options.add_argument("--proxy-bypass-list=*")
#         options.add_argument("--start-maximized")
#         options.add_argument('--disable-gpu')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument('--no-sandbox')

#         # Get URL from form input
#         url = request.POST.get('url')
#         if not url:
#             return HttpResponse("No URL provided.", status=400)

#         # Initialize list to hold metrics data
#         metrics_data = []

#         start = time.time()

#         # Initialize WebDriver and open the measurement site
#         driver = webdriver.Chrome(options=options)
#         driver.get("https://web.dev/measure/")

#         # Input the URL and analyze
#         text_field = driver.find_element(By.NAME, "url")
#         text_field.send_keys(url)
#         button = driver.find_element(By.XPATH, "//button[span[text()='Analyze']]")
#         button.click()

#         # Wait for metrics to load
#         time.sleep(15)

#         # Extract the performance metrics
#         metric_elements = driver.find_elements(By.CSS_SELECTOR, ".OyzgL")
#         lcp_value = inp_value = cls_value = fcp_value = ttfb_value = None

#         for element in metric_elements:
#              metric_text = element.text
#              if "Largest Contentful Paint (LCP)" in metric_text:
#                  lcp_value = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", metric_text)[0])
#              if "Interaction to Next Paint (INP)" in metric_text:
#                  inp_value = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", metric_text)[1])
#              if "Cumulative Layout Shift (CLS)" in metric_text:
#                  cls_value = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", metric_text)[2])
#              if "First Contentful Paint (FCP)" in metric_text:
#                  fcp_value = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", metric_text)[3])
#              if "Time to First Byte (TTFB)" in metric_text:
#                  ttfb_value = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", metric_text)[4])


#         #  Thresholds for each metric
#         thresholds = {
#             "lcp": {"min": 1.7, "max": 19.4, "mean_median_max": 3.9},
#             "inp": {"min": 30, "max": 498, "mean_median_max": 138},
#             "cls": {"min": 0, "max": 5.4, "mean_median_max": 0.065},
#             "fcp": {"min": 1.4, "max": 3, "mean_median_max": 2.65},
#             "ttfb": {"min": 0.5, "max": 1.9, "mean_median_max": 1.55},
#         }

#         # Categorize each metric based on thresholds
#         def categorize(value, metric):
#             if value <= thresholds[metric]["mean_median_max"]:
#                 return "GOOD"
#             elif value <= thresholds[metric]["max"]:
#                 return "OK"
#             else:
#                 return "WORSE"

#         lcp_category = categorize(lcp_value or 4.1, "lcp")
#         inp_category = categorize(inp_value or 30, "inp")
#         cls_category = categorize(cls_value or 5.4, "cls")
#         fcp_category = categorize(fcp_value or 3.0, "fcp")
#         ttfb_category = categorize(ttfb_value or 1.9, "ttfb")

#         # Store metrics and categories in a list
#         metrics_data.append({
#             "url": url,
#             "lcp": {"value": lcp_value, "category": lcp_category},
#             "inp": {"value": inp_value, "category": inp_category},
#             "cls": {"value": cls_value, "category": cls_category},
#             "fcp": {"value": fcp_value, "category": fcp_category},
#             "ttfb": {"value": ttfb_value, "category": ttfb_category},
#         })

       

#         metrics_data = [float(lcp_value), float(inp_value), float(cls_value), float(fcp_value), float(ttfb_value)]

#         # Fixed data points
#         fixed_points = [4.92, 196.9, 2.173, 2.47, 1.33]

#         # Plotting
#         fig, ax = plt.subplots()
#         ax.plot(metrics_data, marker='o', color='b', label="Collected Metrics")
#         ax.plot(fixed_points, marker='x', color='r', linestyle='--', label="Fixed Points")

#         # Set labels and title
#         ax.set_title("Website Performance Metrics")
#         ax.set_xlabel("Metric Index")
#         ax.set_ylabel("Metric Value")
#         ax.legend()

#         # Save plot to in-memory file
#         buffer = io.BytesIO()
#         plt.savefig(buffer, format='png')
#         buffer.seek(0)
#         image_png = buffer.getvalue()
#         buffer.close()

#         # Encode the plot in base64
#         graphic = base64.b64encode(image_png).decode('utf-8')
#         plt.close()

#         # Render in template
#         context = {
#             "metrics_data": metrics_data,
#             "graphic": graphic,
#         }
#         return render(request, "metric_result.html", context)

#     # Render form if GET request
#     return render(request, "metric_input_form_1.html")


def final_score(request):
    if request.method == "POST":
        url = request.POST.get('url')

        try:
            # Metrics from webpage_metrics function
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            links = len(soup.find_all('a', href=True)) + len(soup.find_all('link', href=True))
            body_words = len(soup.find("body").text.split())
            title_length = len(soup.find("title").text)
            graphics = len(soup.find_all("img")) + len(soup.find_all("svg"))
            script_tag = len(soup.find_all("script"))

            metrics = {
                'number_of_link': links,
                'body_text_words': body_words,
                'title_length': title_length,
                'graphics': graphics,
                'number_of_script': script_tag,
            }

            # Sample metrics from analyze_metrics function (replace with actual values)
            lcp_value, inp_value, cls_value, fcp_value, ttfb_value = 3.0, 100, 0.05, 2.5, 1.5

            # Thresholds for normalizing metrics to a 0-100 scale
            thresholds = {
                "lcp": {"max": 4.0},
                "inp": {"max": 200},
                "cls": {"max": 0.1},
                "fcp": {"max": 3.0},
                "ttfb": {"max": 2.0},
                "number_of_link": {"max": 100},
                "body_text_words": {"max": 2000},
                "title_length": {"max": 60},
                "graphics": {"max": 20},
                "number_of_script": {"max": 10},
            }

            # Normalization and scoring
            def normalize(value, metric):
                max_value = thresholds[metric]["max"]
                return min((value / max_value) * 100, 100)

            scores = [
                normalize(lcp_value, "lcp"),
                normalize(inp_value, "inp"),
                normalize(cls_value, "cls"),
                normalize(fcp_value, "fcp"),
                normalize(ttfb_value, "ttfb"),
                normalize(metrics['number_of_link'], "number_of_link"),
                normalize(metrics['body_text_words'], "body_text_words"),
                normalize(metrics['title_length'], "title_length"),
                normalize(metrics['graphics'], "graphics"),
                normalize(metrics['number_of_script'], "number_of_script"),
            ]

            # Final score and categorization
            total_score = sum(scores) / len(scores)
            if total_score >= 90:
                category = "Excellent"
            elif total_score >= 50:
                category = "Good"
            elif total_score >= 25:
                category = "Average"
            else:
                category = "Poor"

            final_metrics = {
                "url": url,
                "total_score": round(total_score, 2),
                "category": category,
                "metrics": metrics,
                "performance_metrics": {
                    "lcp": lcp_value,
                    "inp": inp_value,
                    "cls": cls_value,
                    "fcp": fcp_value,
                    "ttfb": ttfb_value,
                },
            }

            return render(request, 'final_score.html', final_metrics)

        except Exception as e:
            return HttpResponse(f"Error: {e}")

    return render(request, 'metric_input_form_2.html')
