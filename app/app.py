# import necessary libraries and dependencies 
import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
from shinyswatch import theme #for premade UI themes
import palmerpenguins 

# Load dataset into DataFrame for reference throughout out 
df = palmerpenguins.load_penguins()

# Set up the overall page options for the UI- can read more on Shiny- lots of customization options
ui.page_opts(title="Penguins dashboard", fillable=True, theme=theme.vapor)


# Build out user inputs first to debug as needed
# Review shiny components and headers for organization options 
# Update links for accurate URLs based on your project 
with ui.sidebar(title="Filter controls"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/meldstonerogers/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://meldstonerogers.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/meldstonerogers/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Main Content of the app after the sidebar specifications 
with ui.layout_column_wrap(fill=False):
    # Value box to note number of selected penguins
    with ui.value_box(showcase=icon_svg("earlybirds"), style="background-color: #EA39B7"):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal"), style="background-color: #45D9E8"):
        # Value box to note average bill length of selected penguins
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical"), style="background-color: #6F42C1"):
        # Value box to note average bill depth of selected penguins 
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns():
    with ui.card(full_screen=True):
        # Create scatter plot 
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    with ui.card(full_screen=True):
        # Create data grid
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

# Code for custom CSS styling for shiny app 
#ui.include_css(app_dir / "styles.css")

# Define reactive expresssion to filter app based on user input 
@reactive.calc
def filtered_df():
    # Data filtered by species and mass
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
