#include <cstring>

class String
{
public:
    //默认构造，拷贝构造和移动构造
    String(const char *str = nullptr);
    String(const &String other);
    String(String &&other);

    //析构
    ~String();

    //赋值
    String &operator=(char *s);
    String &operator=(String &&other);

private:
    char *str;

}

String::String(char *s)
{
    // corner case
    if (s == nullptr)
    {
        str = new char[1];
        str[0] = '\0';
    }
    else
    {
        str = new char[strlen(s) + 1]; // end operator
        strcpy(str, s);
        str[strlen(s) + 1] = '\0';
    }
}

String::String(const String &other)
{
    int length = strlen(other.str);
    str = new char[length + 1];
    strcpy(str, other.str);
}

String::String(char *s)
{
    // corner case
    if (str == nullptr)
    {
        str = new char[1];
        *str = '\0';
    }
    else
    {
        int length = strlen(s);
        str = new char[length + 1];
        strcpy(str, s);
    }
}

String::String(String &&other)
{
    str = other.str;
    other.str = nullptr;
}

String::~String()
{
    delete[] str;
}

String &String::operator=(char *s)
{
    if (s == nullptr)
    {
        str = new char[1];
        *str = '\0';
    }
    else
    {
        int length = strlen(s);
        str = new char[length + 1];
        strcpy(str, s);
    }
    return *this;
}

String &String::operator=(String &&other)
{
    if(this != &other){
        delete[] str;
        str = other.str;
        other.str = nullptr;
    }

    return *this;
}

