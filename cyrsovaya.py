import sys
import sqlite3
# Библиотеки за для форм
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

# списки с бетоном и арматурой
beton = [('B15', '8.5'), ('B20', '11.5'), ('B25', '14.5'), ('B30', '17'),
         ('B35', '19.5'), ('B40', '22'), ('B45', '25'), ('B50', '27.5'), ('B55', '30'), ('B60', '33')]

armatura = [('A240', '210'), ('A400', '340'), ('A500', '435')]


# Класс формы Результат форма открывается при вычислении
class Calc(QWidget):
    def __init__(self):
        super().__init__()
        self.setting_calc()

    def setting_calc(self):
        uic.loadUi("Calc_form.ui", self)
        self.setWindowTitle('Вычисления')
        self.pushButton.clicked.connect(self.input_A_s)

    # функция для открытия формы с таблицей А_s
    def input_A_s(self):
        self.take_A_s = Asform()
        self.take_A_s.show()

    # функция выводит результат в тектэдит и записывает её в историю
    def returnres(self, result):
        self.textedit.setText(result)
        text = open('txt.txt')
        history = text.read()
        text.close()
        with open('txt.txt', 'w'): pass

        text = open('txt.txt', 'a+')
        text.write(result)
        text.write(history)
        text.close()

    # функция для открытия формы с помощи

# Класс формы Помощь форма открывается при нажатии на кнопку помощь
class Help(QWidget):
    def __init__(self):
        super().__init__()
        self.setting_help()

    def setting_help(self):
        uic.loadUi("Help_form.ui", self)
        self.setWindowTitle('Помощь')
        self.textEdit.setText(
            "Ознакомьтесь с допустимые значениями, для этого нажмите на 'Диапазон допустимых значений'." 
            "Введите переменные и не забудьте выберать класс бетона и арматуры. Нажмите на 'Вычислить'."
            "Для просмотра истории вычислений нажмите на кнопку 'История вычислений'."
            "Для очистки текстового файла используйте кнопку 'Очистить текстовый файл'."
            "Чтобы стереть заполненные вамиполя, нажмите на кнопку 'Очистить заполненные поля'.")
        self.info.clicked.connect(self.info_about)
        self.instuction.clicked.connect(self.instraction_use)
        self.limit.clicked.connect(self.limit_mean)

    # функция при нажатии на кнопку о переменных
    def info_about(self):
        string = "Податливые заделки по концам сечения с размерами b, h, а = а'.\n"\
                "Усилия в опормон сечении от вертикальных нагрузок: продольная сила N, момент M\n"\
                 "Тяжёлый бетон: от B15 до B60 включительно.\n"\
                "Арматура: от A240 до A500 включительно.\n"
        self.textEdit.setText(string)

    # функция при нажатии диапазон допустимых значений
    def limit_mean(self):
        strin = "Допустимые значения в диапазоне от 0 до 10000, включая 0 и 10000"
        self.textEdit.setText(strin)
    # Функция при нажатии на инструкция
    def instraction_use(self):
        self.textEdit.setText(
            "Ознакомьтесь с допустимые значениями, для этого нажмите на 'Диапазон допустимых значений'." 
            "Введите переменные и не забудьте выберать класс бетона и арматуры. Нажмите на 'Вычислить'."
            "Для просмотра истории вычислений нажмите на кнопку 'История вычислений'."
            "Для очистки текстового файла используйте кнопку 'Очистить текстовый файл'."
            "Чтобы стереть заполненные вамиполя, нажмите на кнопку 'Очистить заполненные поля'.")

# Класс с формой таблицы A_s
class Asform(QWidget):
    def __init__(self):
        super().__init__()
        self.setting_asform()

    def setting_asform(self):
        uic.loadUi("Tabl_A_s.ui", self)
        self.setWindowTitle('Таблица значений A_s')

# Класс с формой история вычислоений
class Calc_history(QWidget):
    def __init__(self):
        super().__init__()
        self.settingHistoryCalc()

    def settingHistoryCalc(self):
        uic.loadUi("History_form.ui", self)
        self.setWindowTitle('История вычислений')
# Функция которая записывает в текстовый файл каждое вычисление
    def concatStr(self):
        text = open('txt.txt')
        a = text.read()
        text.close()
        result = a
        self.textedit1.setText(self.textedit1.toPlainText() + result + '\n')

#Класс вычислений открывается форма при нажатии на кнопку вычислиь
class BuildingCalc(QMainWindow):
    def __init__(self):
        super().__init__()
        self.string_result = ''
        self.settingBuildCalc()
        self.res = ''
        self.R_s = 350
        self.R_sc = 350
        self.R_b = 14.5
        self.a = 500
        self.b = 500
        self.h = 500

    def settingBuildCalc(self):
        uic.loadUi("Main_form.ui", self)
        self.setWindowTitle("Проверка прочности опорного сечения колонны")
        # типо при нажатии на кнопки будут работать функции в скобках
        self.calculating.clicked.connect(self.print_result)
        self.history_calc.clicked.connect(self.show_history)
        self.clear.clicked.connect(self.clear_data)
        self.btn_clear_file.clicked.connect(self.clear_file)
        self.help.clicked.connect(self.help_form)
        #Заполняется бетон и арматура значениями в выборке
        for i in beton:
            self.comboBox.addItem(i[0])
        for i in armatura:
            self.comboBox_2.addItem(i[0])

        d = {}
        with open("aAndbAndh.txt") as file:
            for line in file:
                key, *value = line.split()
                d[key] = value
        self.a_list = d.get('a')
        self.b_list = d.get('b')
        self.h_list = d.get('h')

        for i in self.a_list:
            self.comboBox_3.addItem(i)
        for i in self.b_list:
            self.comboBox_4.addItem(i)
        for i in self.h_list:
            self.comboBox_5.addItem(i)


        self.comboBox.activated[str].connect(self.selectcombobeton)
        self.comboBox_2.activated[str].connect(self.selectcomboarmatura)
        self.comboBox_3.activated[str].connect(self.selectcomboa)
        self.comboBox_4.activated[str].connect(self.selectcombob)
        self.comboBox_5.activated[str].connect(self.selectcomboh)
    # заполняется при выборе на форме

    def selectcomboa(self):
        self.meanbox = str(self.comboBox_3.currentText())
        for i in self.a_list:
            if self.meanbox == i:
                self.a = int(i)
    def selectcombob(self):
        self.meanbox = str(self.comboBox_4.currentText())
        for i in self.b_list:
            if self.meanbox == i:
                self.b = int(i)
    def selectcomboh(self):
        self.meanbox = str(self.comboBox_5.currentText())
        for i in self.h_list:
            if self.meanbox == i:
                self.h = int(i)

    def selectcombobeton(self):
        self.meanbox = str(self.comboBox.currentText())
        for i in beton:
            if self.meanbox == i[0]:
                self.R_b = i[1]

    def selectcomboarmatura(self):
        self.meanbox = str(self.comboBox_2.currentText())
        for i in armatura:
            if self.meanbox == i[0]:
                self.R_s = i[1]
                self.R_sc = i[1]
    #функция для взятия результата для вывода в форму вычисления
    def take(self, result):
        self.res1 = result
    #функции открытия формы помощь история вычисления, очистить текстовый файл и поля заполненые на главной форме
    def help_form(self):
        self.help = Help()
        self.help.show()

    def show_history(self):
        self.history_result = Calc_history()
        self.history_result.concatStr()
        self.history_result.show()

    def clear_data(self):
        self.first_size.clear()
        self.second_size.clear()
        self.third_size.clear()
        self.four_size.clear()
        self.five_size.clear()

    def clear_file(self):
        with open('txt.txt', 'w'): pass

    def print_result(self):
        self.calc = Calc()
        self.N = self.third_size.text()
        self.M = self.four_size.text()

        if not self.N.strip() or not self.M.strip():
            self.string_result += ("Проверьте все ли поля заполнены!!!\n\n")
            self.take(self.string_result)

        elif self.N.isdigit() == False or self.M.isdigit() == False:
            self.string_result = ("Не все поля, введённые "
                                  "вами, являются числами!\n")
            self.take(self.string_result)
        elif (float(self.N) < 0 or float(self.N) > 10000) or \
                (float(self.M) < 0 or float(self.M) > 10000) or \
                ((float(self.h) - float(self.a)) - float(self.a)) == 0:

            self.string_result = ("Вы вышли за диапазон допустимых значений,\n"
                                  "пожалуйста ознакомьтесь с допустимыми значениями в разделе Помощь ")
        else:
            self.b = float(self.b)
            self.h = float(self.h)
            self.N = float(self.N)
            self.M = float(self.M)
            self.a = float(self.a)
            self.R_b = float(self.R_b)
            self.R_s = float(self.R_s)
            self.R_sc = float(self.R_sc)
            self.string_result += f"Исходные данные:" \
                                  f" b = {self.b} мм, h = {self.h} мм, a = a' = {self.a} мм " \
                                  f"R_b = {self.R_b} МПа, " \
                                  f"R_s = R_sc = {self.R_s} МПа, " \
                                  f"N = {self.N} кH, M = {self.M} кH*м.\n"
            self.h_0 = self.h - self.a
            self.n_v = 1.0
            self.e = ((self.M*1000)/self.N) + ((self.h_0 - self.a)/2)
            self.a_R = 0.391
            self.E_R = 0.533
            self.N = self.N * 1000
            self.A_S1 = (((self.N) * self.e - self.a_R * self.R_b * self.b * (self.h_0 * self.h_0))
                         / (self.R_sc *(self.h_0 - self.a)))
            self.A_S2 = round( (((self.E_R * self.R_b * self.b * self.h_0 - self.N) / self.R_s) +self.A_S1),1)
            self.string_result += f"Расчет h_0 = {self.h} - {self.a} = {self.h_0} мм. Поскольку момент от ветровой" \
                                  f" нагрузки отсутствует, а согласно 3.2.40 n_v = 1.0, влияние прогиба элемента " \
                                  f"на момент отсутствует. Тогда e = M / N + (a - h_0 / 2) = " \
                                  f"{self.M} * 1000 / {self.N} + {self.h_0} - {self.a} / 2 = {self.e} мм.\n" \
                                  f"Требуемую площадь сечения арматуры S' и S определяем по формулам (3.102) и (3.103)," \
                                  f"Принимая из таблицы 3.3 a_R = 0.391, E_R = 0.533:\n" \
                                  f"A's = (N * e - a_R * R_b * b * h_0^2) / R_sc * (h_0 - a) = {self.N*1000} * {self.e} -" \
                                  f" {self.a_R} * {self.R_b} * {self.b} * {self.h_0}^2 / {self.R_sc} *" \
                                  f" ({self.h_0} - {self.a}) = {self.A_S1}мм^2 > 0,\n" \
                                  f"A_s = ((E_R * R_b * b * h_0 - N) / R_S) + A's = (({self.E_R} * {self.R_b} *" \
                                  f" {self.b} * {self.h_0} - {self.N}) / {self.R_s}) + {self.A_S1} = {self.A_S2} мм^2 > 0.\n"
            if self.A_S2 > 0:
                self.string_result += f"Поскольку оба значения превышают нуль, их не уточняем.\n"
                self.string_result += "Принимаем A_s и A's смотри таблицу.\n"
            else:
                self.A_smin = round(((self.N *(self.h_0 - self.a - self.e))
                               - (self.R_b*self.b*self.h*(self.h/2-self.a))) / (self.R_sc*(self.h_0 - self.a)), 0)
                self.string_result += f"Поскольку A_s не привышает нуль," \
                                      f" площадь сечения арматуры S принимается минимальной по конструктивным" \
                                      f" требованиям, но не менее величины расчитанной по формуле (3.104)\n" \
                                      f"A_s,min = (N * (h_0 - a' - e) - R_b * b * h(h / 2 - a')) / (R_sc(h_0-a'))" \
                                      f" = {self.A_smin}, а площадь сечения араматуры S' определяется:"
                if self.A_smin < 0:
                    self.string_result += f" при отрицательном значении A_s,min по формуле (3.105)"
                else:
                    self.A_S1_new = ((self.N - self.R_b * self.b * self.h)/self.R_sc) - self.A_smin
                    self.string_result += f"при положительном значении A_s, min - по формуле (3.106)\n" \
                    f"A's = N-R_b*b*h/R_sc - As,min = {self.A_S1_new}"
        self.take(self.string_result)
        self.calc.returnres(self.res1)
        self.calc.show()
        self.string_result = ''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BuildingCalc()
    ex.show()
    sys.exit(app.exec())
