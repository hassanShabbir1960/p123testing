def format_report():
    import pandas as pd
    df = pd.read_csv("static/files/Unformatted_file.csv")

    df['Ticker'] = df['Ticker'].str.split(":").str[0]
    df.pop('Unnamed: 0')
    df.pop('Last')
    print("processing done")

    df = df.sort_values('ProjPECurFY',ascending=True)
    import numpy as np

    def is_float(element) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False

    def highlight_cells(val):
        if len(str(val))<7:
            val =str(val)
            color = 'red' if val.find(")")!=-1  else '#000000'
            return 'color: %s' % color
        else:
            val =str(val)
            color = '#000000'
            return 'color: %s' % color
    def bracket_function(val):
        if val < 0:
            return "("+str(abs(val)) +")"
        return str(val)
    def remove_nan(val):
        if str(val)=="nan":
            return ".N/A"
        else:
            return str(val)
    ### MktCap roundoff to 0 decimal places and used thousand seperator
    df['MktCap'] = (np.round(df['MktCap'].values,decimals=0).astype(int))
    df['MktCap'] = df['MktCap'].transform(lambda num: f"{num:,}")

    ### Vol3MAvg roundoff to 0 decimal places 
    df['Vol3MAvg'] = (np.round(df['Vol3MAvg'].values,decimals=0).astype(int))
    ### Pr52 --> end
    ## roundoff to 1 and  used thousand seperator
    ## Change negative sign to () 
    remaining_cols =['Pr52W%Chg', 'Pr4W%Chg', 'Pr4WRel%ChgInd', 'Pr4WRel%Chg',
        'Yield', 'PEExclXorPTM', 'PEG', 'PERelative', 'ProjPECurFY',
        'ProjPENextFY', 'Pr2BookQ', 'Pr2NetFrCashFlTTM', 'Pr2SalesTTM']
    for col in remaining_cols:
        #print(col)
        df[col] = (np.round(df[col].values,decimals=1))
        df[col] =df[col].apply(bracket_function)
        df[col] =df[col].apply(remove_nan)
        


    df.columns = ['Ticker', 'Name', 'Sector Code', 'Ind Code', 'Price', 'MktCap',
        'Vol3M \n Avg', 'Pr52W %Chg', 'Pr4W \n %Chg', 'Pr4W \n Rel \n %Chg \n Ind',
        'Pr4W \n Rel \n %Chg', 'Yield', 'PE \n ExclXor \n PTM', 'PEG', 'PE \n Relative',
        'ProjPE \n CurFY', 'ProjPE \n NextFY', 'Pr2 Book \n Q', 'Pr2 \n FrCashFl \n TTM',
        'Pr2Sales \n TTM']
    
    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y")


    row1 = ["All Stocks fr List Bkttst of DL "+dt_string]+[""]*19
    row_df1 = pd.DataFrame([row1])
    row_df1.columns= ['Ticker', 'Name', 'Sector Code', 'Ind Code', 'Price', 'MktCap',
        'Vol3M \n Avg', 'Pr52W %Chg', 'Pr4W \n %Chg', 'Pr4W \n Rel \n %Chg \n Ind',
        'Pr4W \n Rel \n %Chg', 'Yield', 'PE \n ExclXor \n PTM', 'PEG', 'PE \n Relative',
        'ProjPE \n CurFY', 'ProjPE \n NextFY', 'Pr2 Book \n Q', 'Pr2 \n FrCashFl \n TTM',
        'Pr2Sales \n TTM']

    row2 = [dt_string+""]+[""]*19
    row_df2 = pd.DataFrame([row2])
    row_df2.columns= ['Ticker', 'Name', 'Sector Code', 'Ind Code', 'Price', 'MktCap',
        'Vol3M \n Avg', 'Pr52W %Chg', 'Pr4W \n %Chg', 'Pr4W \n Rel \n %Chg \n Ind',
        'Pr4W \n Rel \n %Chg', 'Yield', 'PE \n ExclXor \n PTM', 'PEG', 'PE \n Relative',
        'ProjPE \n CurFY', 'ProjPE \n NextFY', 'Pr2 Book \n Q', 'Pr2 \n FrCashFl \n TTM',
        'Pr2Sales \n TTM']

    row3 = [""]*20
    row_df3 = pd.DataFrame([row3])
    row_df3.columns= ['Ticker', 'Name', 'Sector Code', 'Ind Code', 'Price', 'MktCap',
        'Vol3M \n Avg', 'Pr52W %Chg', 'Pr4W \n %Chg', 'Pr4W \n Rel \n %Chg \n Ind',
        'Pr4W \n Rel \n %Chg', 'Yield', 'PE \n ExclXor \n PTM', 'PEG', 'PE \n Relative',
        'ProjPE \n CurFY', 'ProjPE \n NextFY', 'Pr2 Book \n Q', 'Pr2 \n FrCashFl \n TTM',
        'Pr2Sales \n TTM']

    df = pd.concat([row_df1,row_df2,row_df3, df], ignore_index=True)
    df
    df.to_excel("static/files/1st.xlsx",index=False)


    # In[38]:


    from datetime import datetime

    # datetime object containing current date and time
    now = datetime.now()
    
    print("now =", now)

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)	


    ## and red color text

    ddf = pd.read_excel("static/files/1st.xlsx")
    ddf.style.applymap(highlight_cells).to_excel("static/files/2nd.xlsx", index=False)

    ## Align right to all columns

    import openpyxl
    import openpyxl.styles
    import string

    from openpyxl import Workbook
    import openpyxl
    w_book = openpyxl.load_workbook('static/files/2nd.xlsx')

    w_sheet = w_book.active
    w_sheet.oddHeader.center.text ="P123_Screen_"+dt_string+"_Jeff_Millennium-ProjCurrPE-sort_2000  tckrs_AAA to ZZZZ.xlsx - \n ProjCurrPE-Order Names AA to Z"
    w_sheet.evenHeader.center.text ="P123_Screen_"+dt_string+"_Jeff_Millennium-ProjCurrPE-sort_2000  tckrs_AAA to ZZZZ.xlsx - \n ProjCurrPE-Order Names AA to Z"

    w_sheet.oddFooter.right.text = "Page &P of &N"
    w_sheet.evenFooter.right.text = "Page &P of &N"

    w_sheet.oddFooter.left.text = "P123_Screen_"+dt_string+"_Jeff_Millennium-ProjCurrPE-sort_2000  tckrs_AAA to ZZZZ.xlsx"
    w_sheet.evenFooter.left.text = "P123_Screen_"+dt_string+"_Jeff_Millennium-ProjCurrPE-sort_2000  tckrs_AAA to ZZZZ.xlsx"

    w_sheet.evenFooter.left.font_size = 8
    w_sheet.oddFooter.left.font_size = 8


    

    w_sheet.print_title_rows = '1:1'  # NOTE this was depricated, old code was ws1.add_print_title(2)
    w_sheet.print_title_cols = 'A:C'  # NOTE: this replaces depricated add_print_title, code was ws2.add_print_title(3, rows_or_cols='cols')
    
    # set the height of the row
    w_sheet.row_dimensions[1].height = 50

    from openpyxl.styles import Alignment



    new_align = Alignment(horizontal='right', vertical='center')  

    def align_cell(w_sheet, col, align):
        for cell in w_sheet[col]:
            cell.alignment = align


    for i in range(102,117):
        col = (chr(i).upper())    
        align_cell(w_sheet, col, new_align)

    from openpyxl.styles import Font
    bold_font = Font(bold=True,name="Calibri",size=11)

    for cell in w_sheet["1:1"]:
        cell.font = bold_font
        cell.alignment = Alignment(horizontal='center', vertical='center')  

    
    w_book.save('static/files/P123_Screen_'+'_Jeff_Millennium-ProjCurrPE-sort_2000  tckrs_AAA to ZZZZ.xlsx')
    w_book.close()
