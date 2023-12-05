# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *


from botcity.plugins.email import BotEmailPlugin

from smtplib import SMTP_SSL

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()

    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to change the default Browser to Firefox
    bot.browser = Browser.FIREFOX

    # Uncomment to set the WebDriver path
    bot.driver_path = R"C:\WebDriver\geckodriver.exe"

    # Opens the BotCity website.
    bot.browse("https://www.infomoney.com.br/cotacoes/cripto/ativo/solana-sol/")
    
    bot.wait(5000)

    # Implement here your logic...
    ...

    if not bot.find( "fechar_Clk", matching=0.97, waiting_time=10000):
        not_found("fechar_Clk")
    bot.click()
    
    bot.wait(3000)
    
    if not bot.find( "valor_Sol", matching=0.97, waiting_time=10000):
        not_found("valor_Sol")
    bot.double_click_relative(91, 110)
    bot.control_c()
    cotacao_Sol = bot.get_clipboard()
    
    print('Valor da Solana > ' + cotacao_Sol)
    
    bot.wait(3000)
    
    if not bot.find( "ck_Fora", matching=0.97, waiting_time=10000):
        not_found("ck_Fora")
    bot.click()
    
    bot.wait(4000)
    
    # Define os dados do e-mail
    from_email = "email aqui"
    to_email = "email aqui"
    subject = "Cotação da Solana"
    body = "O valor atual da Solana é R$" + cotacao_Sol

    # Cria uma conexão com o servidor de e-mail
    smtp = SMTP_SSL("smtp.gmail.com", 465)

    smtp.connect("smtp.gmail.com", 465)
    
    # Faz login no servidor de e-mail
    smtp.login(from_email, "")# chave do e-mail entre aspas

    # Envia o e-mail
    msg = f"Subject: {subject}\n\n{body}"
    msg = msg.encode('utf-8')
    smtp.sendmail(from_email, to_email, msg)

    # Fecha a conexão com o servidor de e-mail
    smtp.quit()

    # Finish and clean up the Web Browser
    # You MUST invoke the stop_browser to avoid
    # leaving instances of the webdriver open
    bot.stop_browser()

    # Uncomment to mark this task as finished on BotMaestro
    # maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.SUCCESS,
    #     message="Task Finished OK."
    # )


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
