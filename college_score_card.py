import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import pandas as pd


def load_data_dict():
    df = pd.read_csv('files/college_scorecard_data_dictionary.csv')
    df_frequency_data = df[['VARIABLE NAME', 'VALUE', 'LABEL']]
    return df_frequency_data


def load_cohort_data():
    df1 = pd.read_csv('files/MERGED2014_15_PP.csv', low_memory=False)
    df2 = pd.read_csv('files/Most-Recent-Cohorts-Treasury-Elements.csv', low_memory=False)
    df = pd.merge(df1, df2, on="UNITID", suffixes=('', '_treasury'))
    return df


def subset_dataframe(df, name):
    sdf = df[df['VARIABLE NAME'] == name]
    return sdf


def data_viz(df, cols, colors, yaxis, ylabel, xlabels):
    # plot correlated values
    plt.rcParams['figure.figsize'] = [16, 6]
    fig, ax = plt.subplots(nrows=1, ncols=len(cols))

    j = 0
    for ax_val in ax:
        ax_val.scatter(df[cols[j]], df[yaxis], alpha=0.5, color=colors[j])
        ax_val.set_xlabel(xlabels[j])
        ax_val.set_ylabel(ylabel)
        ax_val.set_title('Spearman: {}'.format(df[yaxis].corr(df[cols[j]], method='spearman').round(2)))
        j += 1

    plt.show()


if __name__ == '__main__':
    # df_dict = load_data_dict()
    df_cohort_data = load_cohort_data()

    # cohort_columns = df_cohort_data.columns.get_values().tolist()
    #
    # lookup_df = dict()
    # for column in cohort_columns:
    #     slice_df = subset_dataframe(df_dict, column)
    #     if len(slice_df.index) > 1:
    #         lookup_df[column] = slice_df

    # only include schools that are currently operational
    df_included_schools = df_cohort_data[df_cohort_data['CURROPER'] == 1]

    # don't include for-profit schools
    df_included_schools = df_included_schools[
        (df_included_schools['CONTROL'] == 1) |
        (df_included_schools['CONTROL'] == 2)
    ]

    # don't include distance-only schools
    df_included_schools = df_included_schools[(df_included_schools['DISTANCEONLY'] == 0)]

    # include only schools that offer Bachelor, Master and Doctoral degrees
    df_included_schools = df_included_schools[
        (df_included_schools['CCBASIC'] == 14) |
        (df_included_schools['CCBASIC'] == 15) |
        (df_included_schools['CCBASIC'] == 16) |
        (df_included_schools['CCBASIC'] == 17) |
        (df_included_schools['CCBASIC'] == 18) |
        (df_included_schools['CCBASIC'] == 19) |
        (df_included_schools['CCBASIC'] == 20) |
        (df_included_schools['CCBASIC'] == 21) |
        (df_included_schools['CCBASIC'] == 22) |
        (df_included_schools['CCBASIC'] == 23)
    ]

    # don't include schools that did not report admission rate
    df_included_schools = df_included_schools[(df_included_schools['ADM_RATE'].notnull())]

    # don't include schools that did not report SAT AVG
    df_included_schools = df_included_schools[(df_included_schools['SAT_AVG'].notnull())]

    df_included_schools = df_included_schools[
        (df_included_schools['MD_EARN_WNE_P10_treasury'].notnull()) &
        (df_included_schools['MD_EARN_WNE_P10_treasury'] != 'PrivacySuppressed') &
        (df_included_schools['GRAD_DEBT_MDN'] != 'PrivacySuppressed')
    ]

    print("Total school count = {}".format(len(df_included_schools.index)))

    print("Correlation between Admission Rate and Average SAT Score: {}"
          .format(df_included_schools['ADM_RATE']
                  .corr(df_included_schools['SAT_AVG'], method='spearman')))
    print("Correlation between Admission Rate and 6-Year Completion Rate: {}"
          .format(df_included_schools['ADM_RATE']
                  .corr(df_included_schools['D150_4'], method='spearman')))
    print("Correlation between Admission Rate and Median Earning in 10 Years: {}"
          .format(df_included_schools['ADM_RATE']
                  .corr(df_included_schools['MD_EARN_WNE_P10_treasury'], method='spearman')))
    print("Correlation between Student Debt After Graduation and Median Earning in 10 Years: {}"
          .format(df_included_schools['GRAD_DEBT_MDN']
                  .corr(df_included_schools['MD_EARN_WNE_P10_treasury'], method='spearman')))
    print("Correlation between Cost of Attendance and Median Earning in 10 Years: {}"
          .format(df_included_schools['COSTT4_A']
                  .corr(df_included_schools['MD_EARN_WNE_P10_treasury'], method='spearman')))
    print("Correlation between Cost of Attendance and Student Debt After Graduation: {}"
          .format(df_included_schools['COSTT4_A']
                  .corr(df_included_schools['GRAD_DEBT_MDN'], method='spearman')))

    # Visualize correlation between Cost of Attendance
    # and Graduation Debt and Median Earnings after 10 years
    # in a scatter plot
    cols = ['GRAD_DEBT_MDN', 'MD_EARN_WNE_P10_treasury']
    colors = ['#415952', '#f35134']
    data_viz(df_included_schools,
             cols,
             colors,
             'COSTT4_A',
             'Cost of Attendance',
             ['Debt After Graduation', 'Median Earnings In 10 Years'])
