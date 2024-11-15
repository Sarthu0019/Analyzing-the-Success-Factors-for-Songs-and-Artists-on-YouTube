import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_scatter_plot(data_json):
    # Create a scatter plot
    fig, ax = plt.subplots()
    for celeb, values in data_json.items():
        dates, subscribers = zip(*values.items())
        ax.scatter(dates, subscribers, label=celeb)

    ax.set_xlabel('Date')
    ax.set_ylabel('Subscribers')
    ax.legend()

    # Save the plot to a BytesIO object
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    plt.show()
    plt.close()
    # Convert the image data to base64
    base64_img = base64.b64encode(img_data.read()).decode('utf-8')

    return base64_img

# Sample data
sample_data = {
    "Kanye": {"2023-11-09": 778344, "2023-11-10": 778907, "2023-11-11": 779445},
    "gorillaz": {"2023-11-09": 260177, "2023-11-10": 260191, "2023-11-11": 260216},
    "KendrickLamar": {"2023-11-09": 423913, "2023-11-10": 424983, "2023-11-11": 425910},
}

# Generate and show the plot
base64_img = generate_scatter_plot(sample_data)

# Display the image in the notebook
from IPython.display import HTML, display
display(HTML(f'<img src="data:image/png;base64,{base64_img}" alt="Scatter Plot">'))
