# sh comandoPlotsCuts.sh "plot1, plot2" "-E corte1 -E corte2"
# j0 -E mtminse100 -E HH
sh comandoPlotCut.sh "MET, MET_log" "-E j0 -E mtminse100 -E noHH"
sh comandoPlotCut.sh "MET, MET_log" "-E j0 -E mtminse100 -E HH"
sh comandoPlotCut.sh "MET, MET_log" "-E j0 -E mtmin100"
sh comandoPlotCut.sh "MET, MET_log" "-E j1 -E mtminse100 -E noHH"
sh comandoPlotCut.sh "MET, MET_log" "-E j1 -E mtminse100 -E HH"
sh comandoPlotCut.sh "MET, MET_log" "-E j1 -E mtmin100"
