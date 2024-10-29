# In-systems-and-tech

CREATE TABLE Страна (
    id_страны INT PRIMARY KEY,
    название_страны VARCHAR(255) NOT NULL
);

CREATE TABLE Город (
    id_города INT PRIMARY KEY,
    id_страны INT,
    название_города VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_страны) REFERENCES Страна(id_страны)
);

CREATE TABLE Улица (
    id_улицы INT PRIMARY KEY,
    id_города INT,
    название_улицы VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_города) REFERENCES Город(id_города)
);

CREATE TABLE Адрес_поставщика (
    id_адреса INT PRIMARY KEY,
    id_улицы INT,
    дом VARCHAR(10),
    FOREIGN KEY (id_улицы) REFERENCES Улица(id_улицы)
);

CREATE TABLE Поставщик (
    id_поставщика INT PRIMARY KEY,
    фамилия VARCHAR(255),
    имя VARCHAR(255),
    отчество VARCHAR(255),
    телефон VARCHAR(20),
    id_адреса INT,
    FOREIGN KEY (id_адреса) REFERENCES Адрес_поставщика(id_адреса)
);

CREATE TABLE Поставка (
    id_поставки INT PRIMARY KEY,
    id_поставщика INT,
    дата_поставки DATE,
    id_товара INT,
    количество INT,
    FOREIGN KEY (id_поставщика) REFERENCES Поставщик(id_поставщика),
    FOREIGN KEY (id_товара) REFERENCES Товар(id_товара)
);

CREATE TABLE Товар (
    id_товара INT PRIMARY KEY,
    название VARCHAR(255)
);

CREATE TABLE Ценообразование (
    id INT PRIMARY KEY,
    id_товара INT,
    цена DECIMAL(10, 2),
    дата DATE,
    FOREIGN KEY (id_товара) REFERENCES Товар(id_товара)
);

CREATE TABLE Заказчик (
    id_заказчика INT PRIMARY KEY,
    фамилия VARCHAR(255),
    имя VARCHAR(255),
    отчество VARCHAR(255),
    дата_рождения DATE,
    id_адреса INT,
    FOREIGN KEY (id_адреса) REFERENCES Адрес_заказчика(id_адреса)
);

CREATE TABLE Адрес_заказчика (
    id_адреса INT PRIMARY KEY,
    id_улицы INT,
    дом VARCHAR(10),
    FOREIGN KEY (id_улицы) REFERENCES Улица(id_улицы)
);

CREATE TABLE Заказ (
    id_заказа INT PRIMARY KEY,
    дата_заказа DATE,
    id_заказчика INT,
    id_товара INT,
    количество INT,
    FOREIGN KEY (id_заказчика) REFERENCES Заказчик(id_заказчика),
    FOREIGN KEY (id_товара) REFERENCES Товар(id_товара)
);
