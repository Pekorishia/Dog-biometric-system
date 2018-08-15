#include <stdio.h>/**Biblioteca de funções padrão da linguagem C*/
#include <stdlib.h>/**Biblioteca para uso específico de algumas funções*/
#include <string.h>/**Biblioteca para uso de strings*/
#include <ctype.h>/**Biblioteca usada para tratamento de algumas especificidades do programa*/
#include <vector>

/**Variáveis usadas para alocar largura e altura da matriz*/
int altura, largura;

/**Struct com as cores do RGB*/
 typedef struct {
    int r;
    int g;
    int b;
} color;
typedef color Pixel;

/**
 *Gera um novo aquivo .ppm com as devidas alocações de dados.
 */
void gerar_img (std::vector<std::vector<Pixel>> imagem, char saida[]){

    strcat(saida, ".ppm");
    FILE * arq_imagem;
    
    arq_imagem = fopen(saida, "w");

    fprintf(arq_imagem, "P3\n");
    fprintf(arq_imagem, "%i %i\n%i\n",largura, altura, 255);

    int i, j;
    for(i = 0; i < altura; i++){
        for(j = 0; j < largura; j++){
            fprintf(arq_imagem, "%i %i %i\n", imagem[i][j].r, imagem[i][j].g, imagem[i][j].b);
        }
    }    
    fclose(arq_imagem);
}

/**
 *Realiza a binarização da imagem passada com base no threshold informado
 */
std::vector<std::vector<Pixel>> binarization(std::vector<std::vector<Pixel>> imagem, int thr){
    std::vector<std::vector<Pixel>> copy(altura);
    for ( int i = 0 ; i < altura ; i++ )
        copy[i].resize(largura);

    copy = imagem;
    int bin = 0;
    int i, j;

    for(i=0; i < altura; i++){
        for(j=0;j < largura;j++){
            
            bin  = (copy[i][j].r + copy[i][j].g + copy[i][j].b)/3;

            if (bin > thr){
                copy[i][j].r = 255;
                copy[i][j].g = 255;
                copy[i][j].b = 255;
            }else{
                copy[i][j].r = 0;
                copy[i][j].g = 0;
                copy[i][j].b = 0;
            }
        }
    }

    return copy;
}

/**
 *Metodo main onde é carregado o arquivo, mandado para binarizar e salvo em um arquivo .ppm de saida
 */
int main(int argc, char** argv) {   
    
    FILE *arquivo;

    /**Ler o arquivo*/
    arquivo = fopen(argv[1], "r");
    
    /**Faz o teste de erro na abertura do arquivo*/
    /*if(arquivo == NULL){
        printf("%s\n","Erro ao abrir o arquivo de imagem.");
    }else{
        printf("%s\n","Arquivo de imagem aberto com sucesso."); 
    }*/
    
    /**Ler os dados do cabeçalho*/
    fscanf(arquivo, "P3 %i %i 255",&largura, &altura);
    
    /**Cria uma matriz de Pixels*/
    std::vector<std::vector<Pixel>> imagem(altura);
    for ( int i = 0 ; i < altura ; i++ )
        imagem[i].resize(largura);

    /**Ler cada Pixel alocando na variável referente ao struct*/
    for (int i = 0; i < altura; i++)
        for(int j = 0; j < largura; j++)
            fscanf(arquivo, "%i %i %i", &imagem[i][j].r, &imagem[i][j].g, &imagem[i][j].b);

    /**fecha o arquivo*/
    fclose(arquivo);
 
    /**Chama o filtro da binarização*/
    imagem = binarization(imagem, atoi(argv[2]));
    gerar_img(imagem, argv[3]);
    //printf("%s\n", "Imagem binarizada com sucesso.");     
    
    /**Finaliza o programa*/
    return (EXIT_SUCCESS);
}
