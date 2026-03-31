import linkComments
import analyseNotes

cfg_real = "/Users/danjane/Documents/Teaching/Classes/Classes2025/config.yaml"

linkComments.print_suggested_focus(cfg_real)
linkComments.report_dnfs(cfg_real, cut_off=1)

report = linkComments.get_latex_report_from_config_path(cfg_real)
with open("/Users/danjane/Documents/Teaching/Classes/Classes2025/latex/report.tex", "w") as f:
    f.write(report)

analyseNotes.dump_all(cfg_real, "/Users/danjane/Documents/Teaching/Classes/Classes2025/exams/big_dump.xlsx")

