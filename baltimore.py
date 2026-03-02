# `baltimore.py` contains scripts that generate plots of a similar nature to
# those found in the study, except instead of concentrating on national data,
# it focuses on local data (Baltimore, MD). Some of these functions are nearly
# identical to those in `utils.py` (and indeed, some explicitly reference
# `utils.py`). However, because these computations only focus on one city,
# they are, collectively, far lighter and faster to run.

from utils import init
from utils import collect_data_residents
from utils import collect_data_percentile

import matplotlib.pyplot as plt
import numpy as np

# `compute_pwm` computes and returns the population-weighted mean of a given
# `target_data`, usually an air pollutant concentration, for an HOLC-mapped
# block in some area.
def compute_pwm(grade, population_factor, population, target_data):
   # We care only about HOLC-mapped data, so we filter out the lists based
   # on the HOLC grade.
   condition = (~np.equal(grade, 'N'))
   population_factor = population_factor[condition]
   population = population[condition]
   target_data = target_data[condition]
   return np.average(target_data, weights = round(population_factor * population))

# `create_figure_1` collects data and generates six box-and-whisker plots
# displaying the following:
#
# -- Unadjusted population-weighted NO₂ concentration, measured in ppb, among
#    HOLC-graded areas, by HOLC grade and ethnicity, in Baltimore
# -- Intraurban differences in NO₂ concentration, measured in ppb, among
#    HOLC-graded areas, by HOLC grade and ethnicity, in Baltimore
# -- The differences between population-weighted mean NO₂ concentration in
#    Baltimore from the national level
# -- Unadjusted population-weighted PM₂.₅ concentration, measured in μg/m³,
#    among HOLC-graded areas, by HOLC grade and ethnicity, in Baltimore
# -- Intraurban differences in PM₂.₅ concentration, measured in μg/m³, among
#    HOLC-graded areas, by HOLC grade and ethnicity, in Baltimore
# -- The differences between population-weighted PM₂.₅ concentration in
#    Baltimore from the national level
def create_figure_1(local_data, local_no2_pwm, local_pm25_pwm, national_no2_pwm,
                    national_pm25_pwm):

   def collect_data(df, population_factor, target_data, difference):
      HOLC_A_data = []
      HOLC_B_data = []
      HOLC_C_data = []
      HOLC_D_data = []
      white       = []
      other       = []
      black       = []
      asian       = []
      hispanic    = []

      for i in df.index:
         datapoint = [(df[target_data][i]) - difference]
         if df['Grade'][i] == 'A':
            HOLC_A_data += (round(df[population_factor][i] * df['Total'][i]) * datapoint)
         if df['Grade'][i] == 'B':
            HOLC_B_data += (round(df[population_factor][i] * df['Total'][i]) * datapoint)
         if df['Grade'][i] == 'C':
            HOLC_C_data += (round(df[population_factor][i] * df['Total'][i]) * datapoint)
         if df['Grade'][i] == 'D':
            HOLC_D_data += (round(df[population_factor][i] * df['Total'][i]) * datapoint)
         if df['Grade'][i] != 'N':
            white += (round(df[population_factor][i] * df['White'][i]) * datapoint)
            other += (round(df[population_factor][i] * df['Other'][i]) * datapoint)
            black += (round(df[population_factor][i] * df['Black'][i]) * datapoint)
            asian += (round(df[population_factor][i] * df['Asian'][i]) * datapoint)
            hispanic += (round(df[population_factor][i] * df['Hispanic'][i]) * datapoint)
      
      return [HOLC_A_data, HOLC_B_data, HOLC_C_data, HOLC_D_data, white, other,
              black, asian, hispanic]

   def generate_fig_1(data, labels, title, x_label, y_label, min_y, max_y,
                      colors, file_name):
      fig, ax = plt.subplots(nrows = 1, ncols = 1)
      plot = ax.boxplot(data, labels = labels, patch_artist = True,
                        showfliers = False, showmeans = True, vert = True, whis = 0,
                        meanprops = {"marker": "o", "markerfacecolor": "black", "markeredgecolor": "black"})
      ax.set_title(title)
      ax.set_xlabel(x_label)
      ax.set_ylabel(y_label)
      ax.set_ylim(min_y, max_y)
      ax.axhline(y = np.nanmean([elem for lst in data for elem in lst]),
                 color = 'black', linestyle = '--', linewidth = 1, label = 'Overall Mean')
      ax.legend()
      for median in plot['medians']: median.set_color('black')
      for patch, color in zip(plot['boxes'], colors): patch.set_facecolor(color)
      plt.savefig(file_name, dpi = 1200)

   local_no2_data_unadjusted  = collect_data(local_data, 'PHOLC', 'NO2',  0)
   local_no2_data_adjusted    = collect_data(local_data, 'PHOLC', 'NO2',  local_no2_pwm)
   compare_no2_national       = collect_data(local_data, 'PHOLC', 'NO2',  national_no2_pwm)
   local_pm25_data_unadjusted = collect_data(local_data, 'PHOLC', 'PM25', 0)
   local_pm25_data_adjusted   = collect_data(local_data, 'PHOLC', 'PM25', local_pm25_pwm)
   compare_pm25_national      = collect_data(local_data, 'PHOLC', 'PM25', national_pm25_pwm)

   labels  = ['A', 'B', 'C', 'D', 'White', 'Other', 'Black', 'Asian', 'Hispanic']
   x_label = 'HOLC Grade and Race/Ethnicity'
   colors  = ['lightcoral', 'burlywood', 'lightgreen', 'lightskyblue',
            'firebrick', 'orchid', 'darkkhaki', 'darkseagreen', 'cornflowerblue']

   generate_fig_1(local_no2_data_unadjusted, labels,
                  'Baltimore NO₂ Levels: Unadjusted', x_label,
                  'Population-Weighted NO₂ (ppb)', 5, 20, colors,
                  'figure-b1-1.png')
   generate_fig_1(local_no2_data_adjusted, labels,
                  'Baltimore NO₂ Levels: Intraurban Difference', x_label,
                  'Population-Weighted NO₂ (ppb)', -7.5, 7.5, colors,
                  'figure-b1-2.png')
   generate_fig_1(compare_no2_national, labels,
                  'Baltimore NO₂ Levels: National Difference', x_label,
                  'Population-Weighted NO₂ (ppb)', -7.5, 7.5, colors,
                  'figure-b1-3.png')
   generate_fig_1(local_pm25_data_unadjusted, labels,
                  'Baltimore PM₂.₅ Levels: Unadjusted', x_label,
                  'Population-Weighted PM₂.₅ (μg/m³)', 10, 12, colors,
                  'figure-b1-4.png')
   generate_fig_1(local_pm25_data_adjusted, labels,
                  'Baltimore PM₂.₅ Levels: Intraurban Difference', x_label,
                  'Population-Weighted PM₂.₅ (μg/m³)', -1, 1.2, colors,
                  'figure-b1-5.png')
   generate_fig_1(compare_pm25_national, labels,
                  'Baltimore PM₂.₅ Levels: National Difference', x_label,
                  'Population-Weighted PM₂.₅ (μg/m³)', -1, 1.2, colors,
                  'figure-b1-6.png')

# `create_figure_2` collects data and generates four plots displaying the
# following:
#
# -- Intraurban differences in NO₂ concentration, measured in ppb, among
#    HOLC-graded areas, by both HOLC grade _and_ ethnicity, in Baltimore
# -- The differences in NO₂ concentration, measured in ppb, among HOLC-graded
#    areas, by both HOLC grade _and_ ethnicity, between Baltimore and the
#    national level
# -- Intraurban differences in PM₂.₅ concentration, measured in μg/m³, among
#    HOLC-graded areas, by both HOLC grade _and_ ethnicity, in Baltimore
# -- The differences in PM₂.₅ concentration, measured in μg/m³, among
#    HOLC-graded areas, by both HOLC grade _and_ ethnicity, between Baltimore
#    and the national level
def create_figure_2(local_data, local_no2_pwm, local_pm25_pwm,
                    national_no2_pwm, national_pm25_pwm):

   def collect_data(df, population_factor, target_data, pwm):

      def collect_demographic_data(df, population_factor, population,
                                   target_data, pwm):
         A_data = []
         B_data = []
         C_data = []
         D_data = []
         for i in df.index:
            datapoint = (round(df[population_factor][i] * df[population][i]) *
                         [df[target_data][i] - pwm])
            if df['Grade'][i] == 'A':
               A_data += datapoint
            if df['Grade'][i] == 'B':
               B_data += datapoint
            if df['Grade'][i] == 'C':
               C_data += datapoint
            if df['Grade'][i] == 'D':
               D_data += datapoint
         return [np.average(A_data), np.average(B_data), np.average(C_data),
                 np.average(D_data)]

      hispanic = collect_demographic_data(df, population_factor, 'Hispanic', target_data, pwm)
      asian = collect_demographic_data(df, population_factor, 'Asian', target_data, pwm)
      black = collect_demographic_data(df, population_factor, 'Black', target_data, pwm)
      total = collect_demographic_data(df, population_factor, 'Total', target_data, pwm)
      white = collect_demographic_data(df, population_factor, 'White', target_data, pwm)
      return [hispanic, asian, black, total, white]

   def generate_fig_2(data, axes, x_label, y_label, min_y, max_y, file_name):
      fig, ax = plt.subplots()
      ax.plot(axes, data[0], 'g--', label = 'Hispanic')
      ax.plot(axes, data[1], 'b:', label = 'Asian')
      ax.plot(axes, data[2], 'm-', label = 'Black')
      ax.plot(axes, data[3], 'k-', label = 'Total')
      ax.plot(axes, data[4], 'm--', label = 'White')
      ax.axhline(y = 0, color = 'grey', linestyle = '-', linewidth = 1)
      ax.set_xlabel(x_label)
      ax.set_ylabel(y_label)
      ax.set_ylim(min_y, max_y)
      ax.legend()
      plt.savefig(file_name, dpi = 1200)

   local_no2_diff     = collect_data(local_data, 'PHOLC', 'NO2',  local_no2_pwm)
   national_no2_diff  = collect_data(local_data, 'PHOLC', 'NO2',  national_no2_pwm)
   local_pm25_diff    = collect_data(local_data, 'PHOLC', 'PM25', local_pm25_pwm)
   national_pm25_diff = collect_data(local_data, 'PHOLC', 'PM25', national_pm25_pwm)

   axes = ['A', 'B', 'C', 'D']
   x_label = 'HOLC Grade'

   generate_fig_2(local_no2_diff, axes, x_label,
                  'Intraurban NO₂ Difference (ppb)', -6, 6, 'figure-b2-1.png')
   generate_fig_2(national_no2_diff, axes, x_label,
                  'National NO₂ Difference (ppb)', -6, 6, 'figure-b2-2.png')
   generate_fig_2(local_pm25_diff, axes, x_label,
                  'Intraurban PM₂.₅ Difference (μg/m³)', -0.8, 0.8,
                  'figure-b2-3.png')
   generate_fig_2(national_pm25_diff, axes, x_label,
                  'National PM₂.₅ Difference (μg/m³)', -0.8, 0.8,
                  'figure-b2-4.png')

# `create_figure_3` collects data and generates three plots displaying the
# following:
#
# -- The total number of people living in Baltimore, separated by HOLC grade
#    and their respective ethnicities
# -- The proportion of each population living in each HOLC grade that is of
#    a specified ethnicity
# -- Comparison of demographics between Baltimore and the national population
def create_figure_3(all_data, local_data):

   def generate_fig_3_1(weights, width, title, x_label, y_label, y_tick_loc,
                        y_ticks, file_name):
      fig, ax = plt.subplots()
      bottom = np.zeros(4)
      for ethnicity, weight_count in weights.items():
         p = ax.bar(grades, weight_count, width, label = ethnicity, bottom = bottom)
         bottom += weight_count
      ax.set_title(title)
      ax.set_xlabel(x_label)
      ax.set_ylabel(y_label)
      ax.set_yticks(y_tick_loc, y_ticks)
      ax.legend(loc = "upper right")
      plt.savefig(file_name, dpi = 1200)

   def generate_fig_3_2(data, axes, title, x_label, y_label, y_tick_loc, y_ticks, file_name):
      fig, ax = plt.subplots()
      ax.plot(axes, data[0], 'm--', label = 'White')
      ax.plot(axes, data[1], 'k-', label = 'Other')
      ax.plot(axes, data[2], 'm-', label = 'Black')
      ax.plot(axes, data[3], 'b:', label = 'Asian')
      ax.plot(axes, data[4], 'g--', label = 'Hispanic')
      ax.set_title(title)
      ax.axhline(y = 0, color = 'grey', linestyle = '-', linewidth = 1)
      ax.set_xlabel(x_label)
      ax.set_ylabel(y_label)
      ax.set_yticks(y_tick_loc, y_ticks)
      ax.legend(loc = 'upper right')
      plt.savefig(file_name, dpi = 300)

   local_numeric_data, local_percentage_data = collect_data_residents(local_data, 'PHOLC', 10000.0)
   national_numeric_data, national_percentage_data = collect_data_residents(all_data, 'PHOLC', 1000000.0)

   grades = ("A", "B", "C", "D")

   numeric_weights = {
      "White"    : local_numeric_data[0],
      "Other"    : local_numeric_data[1],
      "Black"    : local_numeric_data[2],
      "Asian"    : local_numeric_data[3],
      "Hispanic" : local_numeric_data[4]
   }

   percentage_weights = {
      "White"    : local_percentage_data[0],
      "Other"    : local_percentage_data[1],
      "Black"    : local_percentage_data[2],
      "Asian"    : local_percentage_data[3],
      "Hispanic" : local_percentage_data[4]
   }

   generate_fig_3_1(numeric_weights, 0.65,
                    'Baltimore Resident Demographics in HOLC-Mapped Areas',
                    'HOLC Grade', 'Population (Per 10,000)',
                    (0, 5, 10, 15, 20, 25), (0, 5, 10, 15, 20, 25),
                    'figure-b3-1.png')
   generate_fig_3_1(percentage_weights, 0.65,
                    'Baltimore Resident Demographics in HOLC-Mapped Areas',
                    'HOLC Grade', 'Population (Percentages)',
                    (0, 25, 50, 75, 100), ('0%', '25%', '50%', '75%', '100%'),
                    'figure-b3-2.png')

   national_per = np.array(national_percentage_data)
   diff_per = list(np.subtract(local_percentage_data, national_per))

   generate_fig_3_2(diff_per, ['A', 'B', 'C', 'D'],
                    'Differences in Baltimore and Nationwide Demographics',
                    'HOLC Grade', 'Differences in Population (Percentages)',
                    (-40, -30, -20, -10, 0, 10, 20, 30, 40),
                    ('-40%', '-30%', '-20%', '-10%', '0%', '10%', '20%', '30%', '40%'),
                    'figure-b3-3.png')
   
# `create_figure_4` collects data and generates two plots displaying the
# following:
#
# -- The cumulative distribution of NO₂ concentration, measured in ppb, in
#    Baltimore
# -- The cumulative distribution of PM₂.₅ concentration, measured in μg/m³, in
#    Baltimore
def create_figure_4(local_data):

   def generate_fig_4(data, percentiles, title, x_label, y_label, x_tick_loc,
                      x_ticks, file_name):
      fig, ax = plt.subplots()
      l1 = plt.scatter(percentiles, data[0], s = 5, label = 'HOLC Grade A')
      l2 = plt.scatter(percentiles, data[1], s = 5, label = 'HOLC Grade B')
      l3 = plt.scatter(percentiles, data[2], s = 5, label = 'HOLC Grade C')
      l4 = plt.scatter(percentiles, data[3], s = 5, label = 'HOLC Grade D')
      l5 = plt.scatter(percentiles, data[4], s = 5, label = 'CUA (Census Urbanized Area)')
      ax.set_title(title)
      ax.set_xlabel(x_label)
      ax.set_ylabel(y_label)
      ax.set_xticks(x_tick_loc, x_ticks)
      ax.legend()
      ax.set_axisbelow(True)
      ax.grid(color = "gainsboro")
      plt.savefig(file_name, dpi = 1200)

   baltimore_no2_cum  = collect_data_percentile(local_data, 'PHOLC', 'Total', 'NO2')
   baltimore_pm25_cum = collect_data_percentile(local_data, 'PHOLC', 'Total', 'PM25')
   percentiles = range(0, 100)
   ticks = (0.01, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99.99)

   generate_fig_4(baltimore_no2_cum, percentiles,
                  'Baltimore Cumulative NO₂ Distribution',
                  'Population Percentile', 'NO₂ (ppb)', ticks, ticks,
                  'figure-b4-1.png')
   generate_fig_4(baltimore_pm25_cum, percentiles,
                  'Baltimore Cumulative PM₂.₅ Distribution',
                  'Population Percentile', 'PM₂.₅ (μg/m³)', ticks, ticks,
                  'figure-b4-2.png')

# Nationwide statistics
national_df = init()

# Baltimore statistics
baltimore_df = national_df[national_df['City'] == 'Baltimore, MD']

# Population-weighted mean concentration of NO₂ and PM₂.₅ levels, for both
# Baltimore and nationwide
local_no2_pwm = compute_pwm(baltimore_df['Grade'], baltimore_df['PHOLC'],
                            baltimore_df['Total'], baltimore_df['NO2'])
local_pm25_pwm = compute_pwm(baltimore_df['Grade'], baltimore_df['PHOLC'],
                             baltimore_df['Total'], baltimore_df['PM25'])
national_no2_pwm = compute_pwm(national_df['Grade'], national_df['PHOLC'],
                               national_df['Total'], national_df['NO2'])
national_pm25_pwm = compute_pwm(national_df['Grade'], national_df['PHOLC'],
                                national_df['Total'], national_df['PM25'])

# Comment out whichever plots you don't want to generate so you don't have to
# wait half an hour for it to redo everything
create_figure_1(baltimore_df, local_no2_pwm, local_pm25_pwm, national_no2_pwm, national_pm25_pwm)
create_figure_2(baltimore_df, local_no2_pwm, local_pm25_pwm, national_no2_pwm, national_pm25_pwm)
create_figure_3(national_df, baltimore_df)
create_figure_4(baltimore_df)
