
import dash_html_components as html

layout =html.Div(id='pageContent2',children=[
 	 html.H1("Tutorial Page"),
 	 html.Div(id='tutorialTitle',children=[
 	 		"ESTAÇÕES"]),
 	 html.Div(id='tutorialText',children=[
 	 		"Para fazer o balanceamento das estações na linha de produção, siga os passos abaixo: "]),
 	 html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"1 -   Definir o Takt Time:"]),
 	 		html.Br(),
 	 html.Div(id='tutorialTextcorps',children=[
 	 		"Inserir a duração do turno de trabalho, em horas, e também a eficiência do operador em termos percentuais. Essas duas entradas irão computar o takt time da produção."]),
 	 html.Div(id='tutorialText',children=[
 	 		"2 -   Definir o número de estações na linha de produção."]),
 	 html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"3 -   Entrada das listas de atividades que deverão ser realizadas."]),
 	 html.Div(id='tutorialText',children=[
 	 		"Para isso existem duas vias :"]),
	html.Br(),
 	 html.Div(id='tutorialTextcorps',children=[
 	 		"A -   Upload de um arquivo .csv ou .xls"]),
	html.Br(),
 	  html.Div(id='tutorialTextcorps',children=[
 	 		"O arquivo .csv ou .xls poderá ser inserido arrastando e soltando o arquivo na área de upload ou clicando sobre esta para a seleção do arquivo no computador. É importante ressaltar que a ordem dos dados nas colunas deste arquivo devem ser as especificadas. Após carregamento da planilha os dados deverão aparecer na tabela logo abaixo à área de upload. Nesta tabela ainda é possível editar os dados carregados anteriormente ou ainda acrescentar novas atividades. (Para isto seguir instruções do item b)."]),
html.Br(),
 	 html.Div(id='tutorialTextcorps',children=[
 	 		"B -   Entrada manual dos dados na tabela :"]),
 	 html.Br(),
 	 html.Div(id='tutorialTextcorps',children=[
 	 		" Logo abaixo da área de upload existe uma tabela onde podem ser adicionados manualmente os dados. Para isto basta clicar em “adicionar linha” e alimentar a tabela.  Para editar dados basta selecionar a célula que deseja editar e adicionar a nova informação. Para criar novas linhas na tabela, clicar sobre “ criar linha” e para remover uma linha é preciso apenas clicar sobre o “X” no lado esquerdo da linha da atividade."]),
	html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"4 -   Adicionar os modelos que serão produzidos e quantidades."]), 
html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"5 -   Feito isto o software fará a sugestão das atividades que deverão ser alocadas em cada estação."]),
html.Br(),
	html.A("Tutorial ESTAÇÕES 1", href='https://www.youtube.com/watch?v=TT8KuCXRKJ8&feature=youtu.be', target="_blank"),
	html.Br(),
	html.A("Tutorial ESTAÇÕES 2", href='https://www.youtube.com/watch?v=jbLRArqjYdI&feature=youtu.be', target="_blank"),
##########################################################
	 html.Div(id='tutorialTitle',children=[
 	 		"OPERADORES"]),
	 html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Para fazer a distribuição de tarefas aos operadores, siga os passos abaixo:"]),
 	 html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"1 -   Definir o Takt Time:"]),
 	 		html.Br(),
 	 html.Div(id='tutorialTextcorps',children=[
 	 		"Inserir a duração do turno de trabalho, em horas, e também a eficiência do operador em termos percentuais. Essas duas entradas irão computar o takt time da produção."]),
 	 html.Br(),
 	 html.Div(id='tutorialTextcorps',children=[
 	 		"2 -   Definir o número de estações na linha de produção."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"3 -   Entrada das listas de atividades que deverão ser realizadas."]),
	html.Br(),
 	 html.Div(id='tutorialTextcorps',children=[
 	 		"Para isso existem duas vias:"]),
 	 		html.Br(),
 	 		 html.Div(id='tutorialTextcorps',children=[
 	 		"A -   Upload de um arquivo .csv ou .xls"]),
	html.Br(),
 	  html.Div(id='tutorialTextcorps',children=[
 	 		"O arquivo .csv ou .xls poderá ser inserido arrastando e soltando o arquivo na área de upload ou clicando sobre esta para a seleção do arquivo no computador. É importante ressaltar que a ordem dos dados nas colunas deste arquivo devem ser as especificadas. Após carregamento da planilha os dados deverão aparecer na tabela logo abaixo à área de upload. Nesta tabela ainda é possível editar os dados carregados anteriormente ou ainda acrescentar novas atividades. (Para isto seguir instruções do item b)."]),
html.Br(),
		 html.Div(id='tutorialTextcorps',children=[
 	 		"B -   Entrada manual dos dados na tabela :"]),
 	 html.Br(),
 	 html.Div(id='tutorialTextcorps',children=[
 	 		" Logo abaixo da área de upload existe uma tabela onde podem ser adicionados manualmente os dados. Para isto basta clicar em “adicionar linha” e alimentar a tabela.  Para editar dados basta selecionar a célula que deseja editar e adicionar a nova informação. Para criar novas linhas na tabela, clicar sobre “ criar linha” e para remover uma linha é preciso apenas clicar sobre o “X” no lado esquerdo da linha da atividade."]),
	html.Br(),

 	 html.Div(id='tutorialText',children=[
 	 		"3 -   Adicionar os modelos que serão produzidos e quantidades."]),
html.Br(),
 	 html.Div(id='tutorialTextcorps',children=[
 	 		"Feito isto o software fará a sugestão das atividades que deverão ser alocadas para cada operador."]),
 	 		html.Br(),
 	 		html.A("Tutorial OPERADORES 1", href='https://youtu.be/eodK72IpzN0', target="_blank"),
	html.Br(),
			html.A("Tutorial OPERADORES 2", href='https://www.youtube.com/watch?v=SQkwEOELs4E&feature=youtu.be', target="_blank"),
	html.Br(),
	##########################################
	html.Div(id='tutorialTitle',children=[
 	 		"MIX DE PRODUÇÃO"]),
	
 	 html.Div(id='tutorialText',children=[
 	 		"Para fazer o mix de produção, siga os passos abaixo:"]),
html.Br(),
html.Div(id='tutorialText',children=[
 	 		"1 -   Definir o Takt Time:"]),
 	 		html.Br(),
 	 html.Div(id='tutorialTextcorps',children=[
 	 		"Inserir a duração do turno de trabalho, em horas, e também a eficiência do operador em termos percentuais. Essas duas entradas irão computar o takt time da produção."]),
 	 html.Div(id='tutorialText',children=[
 	 	"2 -   Entrada da lista modelos que deverão ser montados ."]),
 	 		html.Br(),
 	 		html.Div(id='tutorialTextcorps',children=[
 	 		"Para isso existem duas vias:"]),
 	 		html.Br(),
 	 		html.Div(id='tutorialTextcorps',children=[
 	 		"A -   Upload de um arquivo .csv ou .xls"]),
	html.Br(),
 	 html.Div(id='tutorialTextcorps',children=[
 	 		"O arquivo .csv ou .xls poderá ser inserido arrastando e soltando o arquivo na área de upload ou clicando sobre esta para a seleção do arquivo no computador. É importante ressaltar que a ordem dos dados nas colunas deste arquivo devem ser as especificadas. Após carregamento da planilha os dados deverão aparecer na tabela logo abaixo à área de upload. Nesta tabela ainda é possível editar os dados carregados anteriormente ou ainda acrescentar novos modelos. (Para isto seguir instruções do item b)."]),
html.Br(),
		html.Div(id='tutorialTextcorps',children=[
 	 		"B -   Entrada manual dos dados na tabela :"]),
 	 html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"3 -   Feito isto o software fará a sugestão das atividades que deverão ser alocadas para cada operador."]),
html.Br(),
 	 		html.A("Video MIX DE PRODUÇÃO", href='https://www.youtube.com/watch?v=XBeyy7_5igc&feature=youtu.be', target="_blank"),
 	 
 	 ]) 

		
