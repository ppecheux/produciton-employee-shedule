
import dash_html_components as html

layout =html.Div(id='pageContent2',children=[
 	 html.H1("Tutorial Page"),
 	 html.Div(id='tutorialTitle',children=[
 	 		"ESTAÇÕES"]),
 	 html.Div(id='tutorialText',children=[
 	 		"Da página inicial vamos para a parte [então] de estações. "]),
 	 html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Demonstrando um poucoa interface do programa, temos [então] o balanço de estações, onde podemos demonstrar aquantidade de horas que um trabalhador pode estar em turno de trabalho, além da eficiência do trabalhador para mais ou para menos."]),
 	 html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Também podemos alterar a quantidade de estações da linha de produção."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Outro tópico é a lista de atividade de produção, onde podemos fazer por upload arrastando simplesmente os arquivos como ser na imagem e ainda de modo manual adicionando linha por linha de trabalho. "]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Além disso podemos entrar com os produtos necessários e as quantidades de produção, neste caso os produtos seriam os modelos de caminhão."]),
 	 		html.Br(),
 	  html.Div(id='tutorialText',children=[
 	 		"Sendo assim temos a sugestão de estações para os blocos de atividades da linha de produção."]),
 	 		html.Br(),
 	 html.A("Video ESTAÇÕES", href='https://www.youtube.com/watch?v=TT8KuCXRKJ8', target="_blank"),

 	 
 	 html.Div(id='tutorialText',children=[
 	 		"Após definir a quantidade de horas de trabalho, a eficiência do operador e o número de estações, podemos partir [então] para a lista de atividades. Neste exemplo iremos utilizar uma planilha pré-criada podendo ela ser do Excel ou do Google planilhas onde teremos então a definição de produtos, blocos de atividades, duração de atividades e a estação a qual a mesma está fixada."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		" É importante ressaltar que o cabeçalho dessa planilha está exatamente igual como na interface: product, activity block name, activity block duration e fixed station number."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Basta simplesmente realizar o download desta planilha em formato .csv (dados separados por vírgula) e [então], retornando para a interface de trabalho, basta arrastar documento baixado para a interface, logo, temos todos os dados de nossa planilha na interface de trabalho."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Uma questão bastante interessante é que se pode realizar  alterações na planilha de modo livre, mudando quaisquer dados quanto for necessário."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Descendo um pouco mais na interface, temos a quantidade de produtos (neste caso, caminhões) a serem produzidos, sendo assim escolhidos de acordo com a necessidade para as ordens de produção."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Descendo um pouco mais, temos [então] a sugestão de estações para o bloco de atividades."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"O último tópico da interface demonstra de maneira visual como foi definida a sugestão do bloco de atividades."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Porém, caso seja necessário alterações, basta simplesmente voltar ao topo da interface e novamente alterar como necessário, seja esta alteração nas horas de trabalho, no número de estações ou na eficiência do operador, tendo assim novos dados gráficos."]),
 	 		html.Br(),


 	 html.Div(id='tutorialTitle',children=[
 	 		"OPERADORES"]),
 	 html.Div(id='tutorialText',children=[
 	 		"Atentando-se agora a distribuição de tarefas, iremos para interface de operadores. Neste caso temos [então] o tempo de duração de horas do operador além da eficiência de cada operador. Abaixo temos a janela para o arraste de upload da lista de atividades de produção ou ainda adição manual de cada atividade."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Logo abaixo temos a quantidade de caminhões a serem produzidos, como no exemplo anterior, além da sugestão de atividades para cada operador."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Após a seleção das horas de trabalho, além da eficiência de operação, iremos [então] para uma lista pré-construída no Google planilhas ou no Excel com a definição do produto, do bloco de atividade, da duração da atividade, além do número da estação de realização da atividade."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"É importante ressaltar que cada uma das colunas tem como título o nome adequado como descrito na interface."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Para realizar este download basta fazê-lo com a extensão .csv (dados separados por vírgula) e após o download basta apenas arrastar o mesmo até a janela da lista de atividades, tendo assim todas as atividades elencadas como mostrado no vídeo."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"É importante ressaltar que é possível realizar mudanças como sejam necessárias (a qualquer momento)."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Descendo um pouco mais pela interface, conseguimos ainda, quantificar o número de cada modelo de caminhão que será produzido, [então] obtemos a sugestão de atividades para cada operador."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"No final da página verificamos [então] de modo visual como se resulta a distribuição de atividades para cada operador, novamente, mudanças podem ser realizadas caso sejam necessárias, retornando para a tabela que se realizou o upload, mudando as horas de duração e também a eficiência de operação, obtendo assim novos resultados."]),
 	 		html.Br(),


 	 		html.Div(id='tutorialTitle',children=[
 	 		"MIX DE PRODUÇÃO"]),
 	 html.Div(id='tutorialText',children=[
 	 		"Atentando-se a otimização na linha de produção, pensando assim construir a maior quantidade de caminhões, em tempo hábil possível vamos então para a interface do mix de produção."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Neste caso temos então a quantidade de horas trabalhadas além da eficiência do operador. A janela abaixo lista os produtos a serem adicionados de forma a se fazer um upload ou de modo manual, logo tendo então uma sugestão da ordem de produção da linha de caminhões."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"A partir de uma planilha pré selecionada, seja ela no Google planilhas ou no Excel, definindo: o nome ou no caso o modelo do caminhão, o tempo de produção e a quantidade a ser produzida (observa-se que os títulos devem estar idênticos como na interface, fazemos o download do arquivo em extensão csv - dados separados por vírgula)."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Então retornando para a interface, podemos arrastar o arquivo para a janela indicada. É importante ressaltar que mudanças podem ser realizadas nos dados obtidos."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"[Então] temos a ordem de sugestão da linha de produção, o gráfico abaixo demonstra a utilização desta linha de produção a partir de análise de tempo para cada modelo de caminhão fabricado."]),
 	 		html.Br(),
 	 html.Div(id='tutorialText',children=[
 	 		"Ainda é possível fazer alterações apenas com a mudança nos lugares indicados ou até mesmo na planilha criada, obtendo assim diferentes resultados de acordo com a necessidade da planta."]),
 	 		html.Br(),
 	 

 	 ]) 

		