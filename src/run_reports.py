import scripts.som as som
import scripts.liquidweb as liquidweb
import scripts.dewpoint as dewpoint
import scripts.techsmith as techsmith
import modules.module_xlsx_maker as xm
import modules.module_console as con


wb_content = {
    'name': 'job_postings',
    'sheets': []
}

som_worksheet = som.RunScan()
wb_content['sheets'].append(som_worksheet)

liquidweb_worksheet = liquidweb.RunScan()
wb_content['sheets'].append(liquidweb_worksheet)

dewpoint_worksheet = dewpoint.RunScan()
wb_content['sheets'].append(dewpoint_worksheet)

techsmith_worksheet = techsmith.RunScan()
wb_content['sheets'].append(techsmith_worksheet)

con.Info('TASK:\tBuilding Xlsx')

xm.BuildXlsxFile(wb_content)

con.Pass('\033[FPASS:\tXlsx Build Complete')