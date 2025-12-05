class ContaUsuario:
    def __init__(self, email, senha, cargo):
        self.email = email
        self.senha = senha
        self.cargo = cargo

    def autenticar(self, email, senha):
        return (self.email == email) and (self.senha == senha)

    def alterar_senha(self, senha_atual, nova_senha):
        if self.senha == senha_atual:
            self.senha = nova_senha
            print('\u001B[91mSenha trocada com sucesso!\u001B[0m')
        else:
            print('\u001B[91mFalha na troca de senha: senha atual incorreta.\u001B[0m')
