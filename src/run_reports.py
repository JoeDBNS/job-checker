import scripts.som as som
import modules.module_xlsx_maker as xm
import modules.module_console as con


wb_content = {
    'name': 'job_postings',
    'sheets': []
}

som_worksheet = som.RunScan()
wb_content['sheets'].append(som_worksheet)


con.Info('TASK:\tBuilding Xlsx')

xm.BuildXlsxFile(wb_content)

con.Pass('\033[FPASS:\tXlsx Build Complete')