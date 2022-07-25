#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <inttypes.h>

struct record{
    char name[64];    //utf16
    char surname[32]; //utf8
    char gender;
    char email[32];
    char phone_number[16];
    char address[32];
    char level_of_education[8];
    unsigned int income_level; // given little-endian
    unsigned int expenditure;  // given big-endian
    char currency_unit[16];
    char currentMood[32];
    float height;
    unsigned int weight;
};

struct tag{
    char name[5];    //utf16
    char surname[8]; //utf8
    char gender[7];
    char email[6];
    char phone_number[16];
    char address[32];
    char level_of_education[32];
    char income_level[16];
    char expenditure[16];
    char currency_unit[16];
    char currentMood[16];
    char height[16];
    char weight[16];
};

void writingXMLFile(FILE *fxml, struct record recordItem,struct tag tagHead, int id,uint32_t littleEndian,uint32_t bigEndian){
    fprintf(fxml, "\t<row id=\"%d\">\n", id);
    fprintf(fxml, "\t\t<%s>%s</%s>\n", tagHead.name, recordItem.name, tagHead.name);
    fprintf(fxml, "\t\t<%s>%s</%s>\n", tagHead.surname, recordItem.surname, tagHead.surname);
    fprintf(fxml, "\t\t<%s>%c</%s>\n", tagHead.gender, recordItem.gender, tagHead.gender);
    fprintf(fxml, "\t\t<%s>%s</%s>\n", tagHead.email, recordItem.email, tagHead.email);
    fprintf(fxml, "\t\t<%s>%s</%s>\n", tagHead.phone_number, recordItem.phone_number, tagHead.phone_number);
    fprintf(fxml, "\t\t<%s>%s</%s>\n", tagHead.address, recordItem.address, tagHead.address);
    fprintf(fxml, "\t\t<%s>%s</%s>\n", tagHead.level_of_education, recordItem.level_of_education, tagHead.level_of_education);
    fprintf(fxml, "\t\t<%s>%d</%s>\n", tagHead.income_level, recordItem.income_level, tagHead.income_level);
    fprintf(fxml, "\t\t<%s bigEnd=\"%ld\">%d</%s>\n", tagHead.expenditure, littleEndian, bigEndian, tagHead.expenditure);
    fprintf(fxml, "\t\t<%s>%s</%s>\n", tagHead.currency_unit, recordItem.currency_unit, tagHead.currency_unit);
    fprintf(fxml, "\t\t<%s>%s</%s>\n", tagHead.currentMood, recordItem.currentMood, tagHead.currentMood);
    fprintf(fxml, "\t\t<%s>%.2f</%s>\n", tagHead.height, recordItem.height, tagHead.height);
    fprintf(fxml, "\t\t<%s>%d</%s>\n", tagHead.weight, recordItem.weight, tagHead.weight);
    fprintf(fxml, "\t</row>\n");
}

void createXMLFile(FILE *fp){
    FILE *fxml = fopen("/home/kali/Desktop/HW/Output.xml", "w"); //file is opened for writing
    struct record recordItem;
    struct tag tagHead;                                        //create a separate struct for tag

    int counter;int id=0;
    for ( counter=1; counter <= 51; counter++){
        fread(&recordItem, sizeof(recordItem), 1, fp);
        if(counter==1){
            strcpy(tagHead.name, recordItem.name);
            strcpy(tagHead.surname, recordItem.surname);
            strcpy(tagHead.gender, "gender");
            strcpy(tagHead.email, recordItem.email);
            strcpy(tagHead.phone_number, recordItem.phone_number);
            strcpy(tagHead.address, recordItem.address);
            strcpy(tagHead.level_of_education, "level_of_education");
            strcpy(tagHead.income_level, "income_level");
            strcpy(tagHead.expenditure, "expenditure");
            strcpy(tagHead.currency_unit, recordItem.currency_unit);
            strcpy(tagHead.currentMood, recordItem.currentMood);
            strcpy(tagHead.height, "height");
            strcpy(tagHead.weight, "weight");

            if(strcmp(tagHead.name, "name")==0)
                strcpy(tagHead.name, "name");
            if(strcmp(tagHead.surname, "surname")==0)
                strcpy(tagHead.surname, "surname");
            if(strcmp(tagHead.gender, "gender")==0)
                strcpy(tagHead.gender, "gender");
            if(strcmp(tagHead.email, "email")==0)
                strcpy(tagHead.email, "email");
            if(strcmp(tagHead.phone_number, "phone_number")==0)
                strcpy(tagHead.phone_number, "phone_number");
            if(strcmp(tagHead.address, "address")==0)
                strcpy(tagHead.address, "address");
            if(strcmp(tagHead.level_of_education, "level_of_education")!=0)
                strcpy(tagHead.level_of_education, "level_of_education");
            if(strcmp(tagHead.income_level, "income_level")!=0)
                strcpy(tagHead.income_level, "income_level");
            if(strcmp(tagHead.expenditure, "expenditure")!=0)
                strcpy(tagHead.expenditure, "expenditure");
            if(strcmp(tagHead.currency_unit,"currency_unit")==0)
                strcpy(tagHead.currency_unit,"currency_unit");
            if(strcmp(tagHead.currentMood, "currentMood")==0)
                strcpy(tagHead.currentMood, "currentMood");
            if(strcmp(tagHead.height, "height")==0)
                strcpy(tagHead.height, "height");
            if(strcmp(tagHead.weight, "weight")==0)
                strcpy(tagHead.weight, "weight");

            fprintf(fxml, "<records>\n"); 
        }
        else{
            uint32_t littleEndian = recordItem.expenditure;
            uint32_t bigEndian = __builtin_bswap32(littleEndian);
            writingXMLFile(fxml,recordItem,tagHead,id,littleEndian,bigEndian);
        }
        id++;
    }
    fprintf(fxml, "</records>\n"); 
    fclose(fxml);
}

void readFile() {
    FILE *fp;
    fp=fopen("/home/kali/Desktop/HW/records.dat","r");
    if (fp == NULL){
        fprintf(stderr, "\nError opening file\n");
        exit (1);
    }
    createXMLFile(fp);
    fclose(fp);
}

int main() {
    readFile();
    return 0;
}