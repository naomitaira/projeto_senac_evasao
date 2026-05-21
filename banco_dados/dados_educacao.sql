create database dados_educacao;
use dados_educacao;

CREATE TABLE alunos (
    id_aluno INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    sexo CHAR(1),
    data_nascimento DATE,
    renda_familiar DECIMAL(10,2),
    trabalha BOOLEAN
); 

CREATE TABLE cursos (
    id_curso INT PRIMARY KEY AUTO_INCREMENT,
    nome_curso VARCHAR(100),
    nivel VARCHAR(50)
); 

CREATE TABLE matriculas (
    id_matricula INT PRIMARY KEY AUTO_INCREMENT,
    id_aluno INT,
    id_curso INT,
    ano INT,
    semestre INT,
    status ENUM('Ativo','Evadido','Concluído'),
    data_saida DATE,
    motivo_evasao VARCHAR(255),
    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno),
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
); 

CREATE TABLE disciplinas (
    id_disciplina INT PRIMARY KEY AUTO_INCREMENT,
    nome_disciplina VARCHAR(100),
    carga_horaria INT
); 

CREATE TABLE notas (
    id_nota INT PRIMARY KEY AUTO_INCREMENT,
    id_aluno INT,
    id_disciplina INT,
    ano INT,
    semestre INT,
    media DECIMAL(4,2),
    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno),
    FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id_disciplina)
); 

CREATE TABLE frequencia (
    id_frequencia INT PRIMARY KEY AUTO_INCREMENT,
    id_aluno INT,
    id_disciplina INT,
    percentual_frequencia DECIMAL(5,2),
    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno),
    FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id_disciplina)
); 

CREATE TABLE indicadores_completo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ano INT,
    unidade_geografica VARCHAR(50),
    regiao VARCHAR(50),
    localizacao VARCHAR(50),
    dependencia_administrativa VARCHAR(50),
    grupo_de_abandono VARCHAR(50),
    taxa_abandono DECIMAL(5,2),
    renda_media DECIMAL(10,2)
);

CREATE TABLE censo_escolar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ano INT,
    regiao VARCHAR(50),
    uf VARCHAR(10),
    municipio VARCHAR(100),
    instituicao VARCHAR(255),
    dependencia VARCHAR(50)
);
