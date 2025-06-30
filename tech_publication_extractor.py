import pandas as pd

# Load data
data = pd.read_csv('/mnt/raw_data.csv')

print('Basic information of the data:')
data.info()

# Get the number of rows and columns in the dataset
num_rows, num_columns = data.shape

if num_rows < 100 and num_columns < 20:
    # Short table data (less than 100 rows and less than 20 columns) view full data information
    print('Full content information of the data:')
    print(data.to_csv(sep='\t', na_rep='nan'))
else:
    # Long table data view the first few rows of data information
    print('Information of the first few rows of the data:')
    print(data.head().to_csv(sep='\t', na_rep='nan'))

# Define technology types and their corresponding keywords
technology_types = {
    'Endoscopic Examination (EE)': ['endoscopy', 'narrow - band imaging','magnifying endoscopy', 'confocal laser endomicroscopy', 'white - light endoscopy', 'endoscopic submucosal dissection'],
    'Serum Biomarker Detection (SBD)': ['pepsinogen', 'gastrin - 17', 'CA72 - 4', 'CA19 - 9', 'CEA', 'pepsinogen ratio'],
    'Imaging Examination (IE)': ['CT', 'PET - CT', 'MRI', 'diffusion - weighted imaging', 'endoscopic ultrasound', 'barium radiography'],
    'AI - Endoscopy Fusion (AEF)': ['deep learning', 'convolutional neural network', 'computer - aided diagnosis', 'image recognition','real - time analysis','machine learning'],
    'Liquid Biopsy (LB)': ['circulating tumor DNA', 'cell - free DNA', 'extracellular vesicles', 'ctDNA methylation', 'exosomes', 'circulating tumor cells'],
    'Metabolomics Technology (MT)': ['metabolomics', 'lactate dehydrogenase','m2 - PK','metabolic profiling','mass spectrometry','metabolite biomarker'],
    'Microbiomics Technology (MBT)': ['Helicobacter pylori', '16S rRNA', 'Fusobacterium','microbiome', 'gut microbiota','microbial signature'],
    'AI - Based Multi - Omics Integration (AIMI)': ['Helicobacter pylori', '16S rRNA', 'Fusobacterium','microbiome', 'gut microbiota','microbial signature'],
    'Breath Detection Technology (BDT)': ['breath analysis', 'volatile organic compounds', 'electronic nose','sensor technology', 'non - invasive screening']
}

# Create an empty DataFrame to store the results
result = pd.DataFrame(columns=['Publication Year'] + list(technology_types.keys()))

# Get unique values of the year
unique_years = data['Publication Year'].dropna().unique()

# Iterate through each year
for year in unique_years:
    year_data = data[data['Publication Year'] == year]

    # Create an empty dictionary to store the number of publications for each technology type in the current year
    tech_count_dict = {'Publication Year': year}

    # Iterate through each technology type
    for tech, keywords in technology_types.items():
        count = 0

        # Find articles containing keywords of the technology type in the Manual Tags and Abstract Note fields
        for index, row in year_data.iterrows():
            tags = row['Manual Tags'] if isinstance(row['Manual Tags'], str) else ''
            abstract = row['Abstract Note'] if isinstance(row['Abstract Note'], str) else ''

            for keyword in keywords:
                if keyword in tags or keyword in abstract:
                    count += 1
                    break

        tech_count_dict[tech] = count

    # Add the statistical results of the current year to the result DataFrame
    result = pd.concat([result, pd.DataFrame([tech_count_dict])], ignore_index=True)

# Convert the year column to integer type and sort
result['Publication Year'] = result['Publication Year'].astype(int)
result = result.sort_values(by='Publication Year')

print('Number of publications for different technology types each year:')
print(result)
