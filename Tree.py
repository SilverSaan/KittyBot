
import ast
import operator

#Mini Calculadora capaz de adicionar, dividir (Arredondando para baixo), multiplicar e subtrair
#Cria uma arvore de operações para cada npdp
OP_MAP = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.floordiv
}

#Classe que retorna o valor de uma expressão analisada
class Calc(ast.NodeVisitor):
    #Define a visita de cada Nodo (Operador Binario)
    #Para cada nodo visita seu nodo esquerdo e direito. 
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return OP_MAP[type(node.op)](left, right)

    
    #Em caso de visitar um numero, retorna aquele numero. Nodo final da Arvore.
    def visit_Num(self, node):
        return node.n

    #No caso de um nodo ser uma expressão retorna seu valor (Possivelmente outra expressão)
    def visit_Expr(self, node):
        return self.visit(node.value)    
    
    #Chamar esse metodo para avaliar uma expressão: 
    #Exemplo de uso: Calc.evaluate('2 + 5 * 8 / 2 ')
    @classmethod
    def evaluate(cls, expression):
        tree = ast.parse(expression)
        calc = cls()
        return calc.visit(tree.body[0])

def testNode(expression):
    print(Calc.evaluate(expression))

#testNode('2+5*2 * 6')