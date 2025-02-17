import panel as pn
import hvplot.pandas
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

# Load dataset
sleep_df = pd.read_csv("C:/Users/RASICA/PycharmProjects/shl_project/data/sleephealthlifestyle.csv")

# Removing the Person ID column
sleep_df = sleep_df.drop("Person ID", axis=1)

# Data Processing
sleep_df["Sleep Disorder"] = sleep_df["Sleep Disorder"].fillna("None")

# Categorizing Blood Pressure with corrected logic
def categorize_bp(bp):
    if isinstance(bp, str):  # Ensuring bp is a string before processing
        try:
            sys, dia = map(int, bp.split("/"))
            if sys < 90 or dia < 60:
                return "Low"
            elif 90 <= sys <= 119 and 60 <= dia <= 79:
                return "Normal"
            elif 120 <= sys <= 139 or 80 <= dia <= 89:
                return "Elevated"
            elif sys >= 140 or dia >= 90:
                return "High"
            else:
                return "Unknown"
        except ValueError:
            return "Unknown"
    return "Unknown"

sleep_df["BP Category"] = sleep_df["Blood Pressure"].apply(categorize_bp)

# Function to create charts
def create_box_plot(y_axis):
    return sleep_df.hvplot.box(y=y_axis, by="Sleep Disorder", height=400, width=600, cmap="Category10").opts(active_tools=[])

def create_count_plot():
    count_df = sleep_df["Sleep Disorder"].value_counts().reset_index()
    count_df.columns = ["Sleep Disorder", "Count"]
    return count_df.hvplot.bar(x="Sleep Disorder", y="Count", bar_width=0.8, rot=45, height=400, order=["Sleep Apnea", "None", "Insomnia"]).opts(active_tools=[])

def create_corr_heatmap():
    sleep_corr = sleep_df.select_dtypes(include=['int64', 'float64']).corr()
    return sleep_corr.hvplot.heatmap(cmap="Blues", rot=45, height=500).opts(active_tools=[])

def create_bmi_vs_sleep_disorder():
    bmi_count_df = sleep_df.groupby(["BMI Category", "Sleep Disorder"]).size().reset_index(name="Count")
    return bmi_count_df.hvplot.bar(
        x="BMI Category",
        y="Count",
        by="Sleep Disorder",
        stacked=True,
        height=400,
        width=600,
        cmap="Category10",
        legend="top_right"
    ).opts(active_tools=[], xlabel="BMI Category", ylabel="Number of People")

def create_occupation_count_plot():
    count_df = sleep_df.groupby(["Occupation", "Sleep Disorder"]).size().reset_index(name="Count")
    return count_df.hvplot.bar(x="Occupation", y="Count", by="Sleep Disorder", stacked=True, height=400, width=1200, cmap="Category10", legend="top_right").opts(active_tools=[], xlabel="Occupation", ylabel="Count")

# Updated BMI vs Blood Pressure Chart
def create_bmi_vs_bp_chart():
    bmi_bp_df = sleep_df.groupby(["BMI Category", "BP Category"]).size().reset_index(name="Count")
    return bmi_bp_df.hvplot.bar(
        x="BMI Category",
        y="Count",
        by="BP Category",
        stacked=True,
        height=400,
        width=700,
        cmap="Category10",
        legend="top_right"
    ).opts(active_tools=[], xlabel="BMI Category", ylabel="Count", title="BMI Category vs Blood Pressure")

# Key Insights Page
def create_key_insights():
    insights = """
    ## Key Insights:
    **1.** Approximately **87% of overweight individuals** suffer from sleep disorders, with **43.2%** experiencing **insomnia** and **43.9%** experiencing **sleep apnea.** <br><br>
    **2.** **83% of nurses** suffer from **sleep apnea** and exhibit **high physical activity levels.** <br><br>
    **3.** Individuals with **high physical activity levels (above ~78)** are more likely to **suffer from sleep apnea,** as **excessive physical exertion** can lead to **exhaustion.** <br><br>
    **4.** A **high stress level** correlates with an **increased heart rate (+0.67).** <br><br>
    **5.** i. **High stress levels** lead to **lower sleep quality** and **shorter sleep duration.** <br><br>
           ii. **Higher heart rates** are associated with **poor sleep quality,** showing opposing trends to normal sleep patterns. <br><br>
    **6.** Nearly **99.99%** of individuals classified as **obese** or **overweight** suffer from either **sleep apnea** or **insomnia.** <br><br>
    """
    return pn.Column(pn.pane.Markdown(insights, width=650), align="center")

# Apply Custom Font via CSS
pn.config.raw_css.append("""
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

body, .bk-root {
    font-family: 'Poppins', sans-serif !important;
}

.bk-panel-title {
    font-weight: 600;
    font-size: 20px;
}
""")

# Widgets
button_width = 170
buttons = [
    pn.widgets.Button(name="Introduction", button_type="primary", width=button_width),
    pn.widgets.Button(name="Dataset", button_type="primary", width=button_width),
    pn.widgets.Button(name="Sleep Disorder Count", button_type="primary", width=button_width),
    pn.widgets.Button(name="Correlation", button_type="primary", width=button_width),
    pn.widgets.Button(name="Feature Distribution", button_type="primary", width=button_width),
    pn.widgets.Button(name="BMI vs Sleep Disorder", button_type="primary", width=button_width),
    pn.widgets.Button(name="BMI vs Blood Pressure", button_type="primary", width=button_width),
    pn.widgets.Button(name="Occupation Count", button_type="primary", width=button_width),
    pn.widgets.Button(name="Key Insights", button_type="primary", width=button_width),
]

y_axis_box = pn.widgets.Select(name="Y-Axis", options=list(sleep_df.select_dtypes(include=['int64', 'float64']).columns), value="Sleep Duration")

# Page Layouts
def CreatePage1():
    descr = """
        ## This interactive dashboard analyses factors affecting sleep disorders through various visualizations, providing insights into key metrics such as sleep duration, stress levels, physical activity, and overall health trends.  
        ## The dataset contains around ~300 records  with the following features and their data types.
        **Gender**: object <br>
        **Age**: int64 <br>
        **Occupation**: object <br>
        **Sleep Duration**: float64 <br>
        **Quality of Sleep**: int64 <br>	 
        **Physical Activity Level**: int64 <br>	
        **Stress Level**: int64 <br>
        **BMI Category**: object <br>
        **Blood Pressure**: object <br>
        **Heart Rate**: int64 <br>
        **Daily Steps**: int64 <br>
        **Sleep Disorder**: object <br>
        """
    return pn.Column(pn.pane.Markdown(descr, width=550), align="center")

def CreatePage2():
    return pn.Column(pn.pane.Markdown("## Dataset Explorer"), pn.pane.DataFrame(sleep_df, height=450, width=850), align="center")

def CreatePage3():
    return pn.Column(pn.pane.Markdown("## Sleep Disorder Count"), create_count_plot(), align="center")

def CreatePage4():
    return pn.Column(pn.pane.Markdown("## Correlation Heatmap"), create_corr_heatmap(), align="center")

def CreatePage5():
    return pn.Column(pn.pane.Markdown("## Box Plot of Features by Sleep Disorder"), y_axis_box, pn.bind(create_box_plot, y_axis_box), align="center")

def CreatePage6():
    return pn.Column(pn.pane.Markdown("## BMI Category vs Sleep Disorder"), create_bmi_vs_sleep_disorder(), align="center")

def CreatePage7():
    return pn.Column(pn.pane.Markdown("## BMI Category vs Blood Pressure"), create_bmi_vs_bp_chart(), align="center")

def CreatePage8():
    return pn.Column(pn.pane.Markdown("## Occupation Count Plot"), create_occupation_count_plot(), align="center")

def CreatePage9():
    return create_key_insights()

# Mapping for Pages
mapping = {
    "Page1": CreatePage1(),
    "Page2": CreatePage2(),
    "Page3": CreatePage3(),
    "Page4": CreatePage4(),
    "Page5": CreatePage5(),
    "Page6": CreatePage6(),
    "Page7": CreatePage7(),
    "Page8": CreatePage8(),
    "Page9": CreatePage9(),
}

# Function to Switch Pages
def show_page(page_key):
    main_area.clear()
    main_area.append(mapping[page_key])

# Button Click Event Binding
for i, page_key in enumerate(mapping.keys()):
    buttons[i].on_click(lambda event, pk=page_key: show_page(pk))

# Sidebar & App Layout
sidebar = pn.Column(pn.pane.Markdown("## Pages"), *buttons, styles={"width": "100%", "padding": "15px"})
main_area = pn.Column(mapping["Page1"], styles={"width": "100%"})
template = pn.template.VanillaTemplate(title="Sleep Disorder Analysis", sidebar=[sidebar], main=[main_area])
template.servable()
