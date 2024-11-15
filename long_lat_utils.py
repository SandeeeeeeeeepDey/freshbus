from tqdm.auto import tqdm

dict_to_get_long_lat_from = {'Nayandahalli': (12.9417695999146, 77.5251083374023),
 'Tin factory': (12.9972496032715, 77.6698608398438),
 'ITI Gate': (13.0057001113892, 77.6855773925781),
 'K R Puram': (13.0064897537231, 77.6877365112305),
 'Hoskote': (13.0705404281616, 77.783821105957),
 'Halasuru': (12.9764204025269, 77.626708984375),
 'Indiranagar': (12.9827699661255, 77.6378402709961),
 'RTC Bus Stand(NEW DOT TRAVELS)': (13.6285305023193, 79.4261703491211),
 'Swami Vivekananda': (12.9854898452759, 77.6442337036133),
 'Majestic Bus Station': (12.9763298034668, 77.5749893188477),
 'Kapilatheertham busstop': (13.6531600952148, 79.4209899902344),
 'Alipiri bus stop': (13.6462497711182, 79.4050674438477),
 'Cherlopalli bus stop': (13.6140995025635, 79.3631286621094),
 'Chandragiri Busstop': (13.5881404876709, 79.3160781860352),
 'Chitoor Bypass': (0.0, 0.0),
 'Lalbagh': (12.9551095962524, 77.5857391357422),
 'Silk Board Junction': (12.9179801940918, 77.6221237182617),
 'HSR Layout': (12.9165897369385, 77.6349563598633),
 'Bellandur': (12.9278202056885, 77.6803665161133),
 'Marathahalli Multiplex': (12.9515695571899, 77.6996231079102),
 'Mahadevpura': (12.9887599945068, 77.6888580322266),
 'Eblur Junction': (12.9209499359131, 77.6659622192383),
 'Marathahalli Kalamandir': (12.9911003112793, 77.6875991821289),
 'Anand Rao Circle': (12.9801597595215, 77.5750198364258),
 'RTC Busstand(Srinivasam cmplx)': (13.631739616394, 79.4288177490234),
 'Baiyyappanahalli': (0.0, 0.0),
 'Leela Mahal BUS STOP': (0.0, 0.0),
 'Corporation Circle': (0.0, 0.0),
 'Maruthi Mandir': (12.9679098129273, 77.5361709594727),
 'Attiguppe': (0.0, 0.0),
 'Vijayanagar': (12.9706401824951, 77.5391235351563),
 'Rajajinagar ISKCON Temple': (13.0115699768066, 77.5512771606445),
 'Rajajinagar': (12.9990396499634, 77.5539321899414),
 'ChitToor Bypass-Iruvaram cpost': (13.1979103088379, 79.0648574829102),
 'Shanti Nagar': (12.9540395736694, 77.5908737182617),
 'Wilson garden': (12.9492702484131, 77.5976181030273),
 'St Johns Hospital': (12.9300603866577, 77.6151733398438),
 'Bharath Nagar': (17.4675102233887, 78.428108215332),
 'Erragada': (17.4537105560303, 78.4343566894531),
 'Panjagutta': (17.4286003112793, 78.4504776000977),
 'Lakdikapool': (17.4072399139404, 78.4661102294922),
 'Ramoji Film City': (17.3115501403809, 78.6826782226563),
 'Ibrahimpatnam': (16.5891609191895, 80.5193634033203),
 'Gollapudi': (16.5447406768799, 80.5788803100586),
 'Nizampet': (17.4985198974609, 78.3894271850586),
 'Bhavanipuram': (16.5258693695068, 80.5936126708984),
 'Mangalagiri Bypass': (16.426700592041, 80.5780563354492),
 'Raintree Park Namburu': (16.3760108947754, 80.5175170898437),
 'Tadepalli': (16.4848499298096, 80.6199188232422),
 'Benz Circle': (16.4967498779297, 80.6528472900391),
 'Police control room': (16.5113792419434, 80.6188735961914),
 'Kukatpally': (17.4831390380859, 78.4140777587891),
 'Wipro Circle': (17.4275398254394, 78.3417510986328),
 'IIIT Hyderabad': (17.4463901519775, 78.3514862060547),
 'Nallagandla Flyover': (17.4798393249512, 78.3168106079102),
 'Koti': (17.3851642608643, 78.4850540161133),
 'Malakpet': (17.3734397888184, 78.5026397705078),
 'Dilsukhnagar': (17.3687496185303, 78.5263290405274),
 'Kothapet': (17.3675708770752, 78.5391464233399),
 'L B Nagar Metro Station': (17.3498706817627, 78.5480270385742),
 'L B Nagar-MRF Showroom': (0.0, 0.0),
 'Vanasthalipuram': (17.3375797271729, 78.5701522827148),
 'SR Nagar': (17.4415397644043, 78.4417114257812),
 'Ameerpet': (17.4305801391602, 78.4485931396484),
 'BHEL X Roads': (17.5028705596924, 78.31201171875),
 'RTC Bus Stand': (16.5072898864746, 80.6157989501953),
 'KPHB': (17.4915008544922, 78.4063568115234),
 'Chandanagar': (17.4952793121338, 78.3236694335938),
 'Madeenaguda': (17.4952907562256, 78.3465881347656),
 'Allywn CrossRoads': (17.4936695098877, 78.3506927490234),
 'Miyapur X Roads': (17.4971008300781, 78.3625030517578),
 'Varadhi': (16.5020294189453, 80.6339797973633),
 'Namburu Underpass': (16.3743991851807, 80.5158081054688),
 'LB Nagar Shah Ghouse Hotel': (17.3435001373291, 78.5559387207031),
 'Kakani Road': (16.3041496276856, 80.4609222412109),
 'NTR CIRCLE RTC Bus Stand': (16.2967300415039, 80.4560165405274),
 'Abids': (17.3874893188477, 78.4774703979492),
 'Gachibowli': (17.4373455047607, 78.3629531860352),
 'L B Nagar': (17.3455390930176, 78.5519104003906),
 'Nampally': (17.3921699523926, 78.470100402832),
 'NTR Circle': (16.2941799163818, 80.4543609619141),
 'Indira Nagar': (17.4407138824463, 78.3611068725586),
 'Gachibowli Stadium': (17.4492740631104, 78.3487396240234),
 'Benz Circle - Reliance trends': (16.4980907440186, 80.652717590332),
 'Benz Circle - Prasanna Travels': (16.4967498779297, 80.6528472900391),
 'Kondapur RTO Office': (17.4715518951416, 78.3651504516602),
 'Hayathnagar': (17.3280372619629, 78.6017074584961),
 'Kondapur': (17.4617099761963, 78.3671646118164),
 'CHITOOR BYPASS JN(80KM FRM TIRUPATI)': (13.1979103088379, 79.0648574829102),
 'Allwyn X Roads': (17.492639541626, 78.3528137207031),
 'ISB Road Junction': (17.4446887969971, 78.3524551391602),
 'CHITOOR BYPASS JN-KM FRM TPT': (13.1971597671509, 79.0643768310547),
 'Chandragiri Bypass': (13.5782442092896, 79.3107070922852)}

# Delete Experiment
def get_long_lat(m_df, boarding:str, stoppage:str):
    for inx, row in tqdm(m_df.iterrows(), total=len(m_df)):
        blong_list = []
        blat_list = []
        for i in row[f"{boarding}_name"]:
            blong_list.append(dict_to_get_long_lat_from[i][1])
            blat_list.append(dict_to_get_long_lat_from[i][0])
        m_df.at[inx, f"{boarding}_long"] = f"{blong_list}"
        m_df.at[inx, f"{boarding}_lat"] = f"{blat_list}"
        slong_list = []
        slat_list = []
        for i in row[f"{boarding}_name"]:
            slong_list.append(dict_to_get_long_lat_from[i][1])
            slat_list.append(dict_to_get_long_lat_from[i][0])
        m_df.at[inx, f"{boarding}_long"] = f"{slong_list}"
        m_df.at[inx, f"{boarding}_lat"] = f"{slat_list}"
    return m_df