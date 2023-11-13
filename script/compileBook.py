import subprocess
import os
import re
from functools import reduce

BANNER1 = r"""
  _____                                          ____              _    
 / ____|                                        |  _ \            | |   
| (___   ___  ___ _   _ _ __ ___ _   _ _ __ ___ | |_) | ___   ___ | | __
 \___ \ / _ \/ __| | | | '__/ _ \ | | | '_ ` _ \|  _ < / _ \ / _ \| |/ /
 ____) |  __/ (__| |_| | | |  __/ |_| | | | | | | |_) | (_) | (_) |   < 
|_____/ \___|\___|\__,_|_|  \___|\__,_|_| |_| |_|____/ \___/ \___/|_|\_\
  _____                      _ _ 
 / ____|                    (_) |          
| |     ___  _ __ ___  _ __  _| | ___ _ __ 
| |    / _ \| '_ ` _ \| '_ \| | |/ _ \ '__|
| |___| (_) | | | | | | |_) | | |  __/ |   
 \_____\___/|_| |_| |_| .__/|_|_|\___|_|   
                      | |                  
                      |_|                  
"""
BANNER2 = r"""
  _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _  
 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
( F | e | t | c | h | i | n | g | f | i | l | e | s | . | . | . )
 \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ 
"""
BANNER3 = r"""
  _   _   _   _   _   _   _   _   _   _   _   _   _  
 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
( A | p | p | l | y | i | n | g | f | i | x | e | s )
 \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ 
"""
BANNER4 = r"""
  _   _   _   _   _   _   _   _   _   _   _   _  
 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
( L | a | T | e | X | C | o | m | p | i | l | e )
 \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ 
"""
BANNER5 = r"""
  _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _  
 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
( L | a | T | e | X | C | o | m | p | i | l | e | A | g | a | i | n )
 \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ 
"""
BANNER6 = r"""
  _   _   _   _   _   _   _  
 / \ / \ / \ / \ / \ / \ / \ 
( C | l | e | a | n | u | p )
 \_/ \_/ \_/ \_/ \_/ \_/ \_/ 
"""
BANNER7 = r"""
 _____                     _
|  __ \                   | |
| |  | | ___  _ __   ___  | |
| |  | |/ _ \| '_ \ / _ \ |_|
| |__| | (_) | | | |  __/  _
|_____/ \___/|_| |_|\___| (_)
"""

def fetchFiles():
    parentdir = "../src/learn/"
    subdirs = [
        directory
        for directory in os.listdir(parentdir)
        if not(directory.endswith(".md"))
    ]

    files =(
        [
            os.path.join(parentdir, directory, file)
            for directory in subdirs
            for file in sorted(
                os.listdir(os.path.join(parentdir, directory)),
                key=extractNumber 
            )
            if not(file.startswith("Summary_"))
        ]
    )

    return files

def executePandoc(mdFile):

    filename = os.path.basename(mdFile)

    texfile = os.path.join(
        "./texfiles",
        filename.replace(".md", ".tex")
    )

    subprocess.call([
        "pandoc", mdFile, "-o", texfile, "--lua-filter=./luaFilters/codeblock_filter.lua"
    ])

    return texfile


def extractNumber(filename):
    match = re.search(r'^(\d+)(?:\.(\d+))?_(.+)$', filename)
    if match:
        prefix = int(match.group(1))
        major_version = int(match.group(2)) if match.group(2) else 0
        minor_version = match.group(3)
        return prefix, major_version, minor_version
    return float('inf'), float('inf'), filename

def fixImages(texFiles):

    for texFile in texFiles:

        with open(texFile) as file:
            content = file.read()
            pattern = r"\\includegraphics{([^}]*)}"
            matches = map(
                lambda x: (x, x.replace("/../img/", "/src/img/")),
                re.findall(pattern, content)
            )
            for match, fixed in matches:
                content = content.replace(match, fixed)
            content = content.replace(
                r"\includegraphics{",
                r"\includegraphics[width=\linewidth]{"
            )

        with open(texFile, "w") as file:
            file.write(content)

def fixSlashedN(texFiles):
    
    for texFile in texFiles:

        with open(texFile) as file:
            content = file.read().replace("ᵰ", r"\stkout{n}")

        with open(texFile, "w") as file:
            file.write(content)

def fixInlineMath(texFiles):

    pattern = r"\n\$(.*?)\$\n"

    for texFile in texFiles:

        with open(texFile) as file:
            content = file.read()
            content = re.sub(
                pattern,
                '\n\\[\\1\\]\n',
                content
                .replace(r"\[", "$")
                .replace(r"\]", "$")
            )

        with open(texFile, "w") as file:
            file.write(content)

def fixPowFormula(texfiles):

    for texFile in texFiles:

        with open(texFile) as file:
            content = file.read()
            content = (
                content
                .replace(
                    r"""$
(m,n)=\text{PoW}\left(H_{\stkout{n}},H_n,d\right)\\ m=H_m\wedge n\leq\frac{2^{256}}{H_d}
$""",
                    r"""\begin{align*}
(m,n)&=\text{PoW}\left(H_{\stkout{n}},H_n,d\right)\\ m&=H_m\wedge n\leq\frac{2^{256}}{H_d}
\end{align*}""",
                )
                .replace(
                    r"""\[\mu_s'[0]=\text{KEC}\left(\mu_m\left[\mu_s[0]\left(\mu_s[0]+\mu_s[1]-1\right)\right]\right)\\ \mu_i'=\text{M}\left(\mu_i,\mu_s[0],\mu_s[1]\right)\]""",
                    r"""\begin{align*}
\mu_s'[0]&=\text{KEC}\left(\mu_m\left[\mu_s[0]\left(\mu_s[0]+\mu_s[1]-1\right)\right]\right)\\
\mu_i'&=\text{M}\left(\mu_i,\mu_s[0],\mu_s[1]\right)
\end{align*}"""
                )
            )

        with open(texFile, "w") as file:
            file.write(content)


def changeCodeBlocks(texFiles):

    for texFile in texFiles:

        with open(texFile) as file:
            content = file.read()
            content = (
                content
                .replace(
                    r"""\begin{Shaded}
\begin{Highlighting}[]""",
                    r"\begin{lstlisting}[language=Solidity,numbers=none]"
                )
                .replace(
                    r"""\end{Highlighting}
\end{Shaded}""",
                    r"\end{lstlisting}"
                )
            )

        pattern = r'\\NormalTok{([^{}]*)}'
        content = re.sub(pattern, r'\1', content)

        with open(texFile, "w") as file:
            file.write(content)

def setChapters(texFiles):

    for file in texFiles:
        with open(os.path.join("./texfiles/", file)) as f:
            content = f.read().replace(r"\section{", r"\chapter{")
    
        with open(os.path.join("./texfiles/", file), "w") as f:
            f.write(content)

if __name__ == "__main__":
    ## Open issues
    # portada?
    # preface?
    # epilogue?
    # doi en zenodo

    print(BANNER1)

    print("\n\n" + 80*"#")
    print(BANNER2)

    os.system("mkdir ./texfiles/")

    texFiles = []

    for file in fetchFiles():

        texfile = executePandoc(file)

        print(f"Executed {texfile}")

        texFiles.append(texfile)

    setChapters(filter(
        lambda x: x.split("_")[0].isdigit(),
        os.listdir("./texfiles/")
    ))

    print("\n\n" + 80*"#")
    print(BANNER3)

    fixImages([
        "./texfiles/1.4_Ethereum_core_components.tex"
    ])

    fixSlashedN([
        "./texfiles/1.4_Ethereum_core_components.tex"
    ])

    fixInlineMath([
        "./texfiles/1.1_Ethereum_Concept.tex",
        "./texfiles/1.4_Ethereum_core_components.tex",
        "./texfiles/1.10_Transactions_Properties_and_Components.tex",
        "./texfiles/1.14_Transaction_Reverts_and_Data.tex",
        "./texfiles/1.16_Mainnet_and_Testnets.tex",
        "./texfiles/2.11_Solidity_Variables.tex",
        "./texfiles/2.15_Solidity_Units.tex",
        "./texfiles/2.28_Open_Zeppelin_Libraries.tex",
        "./texfiles/2.30_Important_Protocols.tex",
        "./texfiles/4.1_Audit.tex"
    ])

    fixPowFormula([
        "./texfiles/1.4_Ethereum_core_components.tex",
    ])

    # changeCodeBlocks([
    #     "./texfiles/1.13_EVM_in_Depth.tex",
    #     "./texfiles/2.2_SPDX_and_Pragmas.tex",
    #     "./texfiles/2.3_Imports.tex",
    #     "./texfiles/2.4_Comments_and_Natspec.tex",
    #     "./texfiles/2.8_Functions.tex",
    #     "./texfiles/2.9_Events.tex",
    #     "./texfiles/2.11_Solidity_Variables.tex",
    #     "./texfiles/2.15_Solidity_Units.tex",
    #     "./texfiles/2.18_Error_Handling.tex",
    #     "./texfiles/2.28_Open_Zeppelin_Libraries.tex",
    #     "./texfiles/2.22_Inheritance.tex",
    #     "./texfiles/2.28_Open_Zeppelin_Libraries.tex"
    # ])

    with open("./templates/secureumBookTemplate.tex") as file:
        template = file.read()

    base = template.replace(
        "%%%ELLIPSIS%%%",
        reduce(
            lambda x, y: x + y,
            map(
                lambda x: r"\input{" + x + "}\n",
                texFiles
            )
        )
    )

    with open("./texfiles/secureumBootcamp.tex", "w") as file:
        file.write(base)

    print("\n\n" + 80*"#")
    print(BANNER4)

    subprocess.call([
        "xelatex",
        "./texfiles/secureumBootcamp.tex"
    ])

    print("\n\n" + 80*"#")
    print(BANNER5)
    # Twice to get the TOC
    subprocess.call([
        "xelatex",
        "./texfiles/secureumBootcamp.tex"
    ])

    print("\n\n" + 80*"#")
    print(BANNER6)
    os.system("mv ./secureumBootcamp.pdf ../.")
    # os.system("rm -rf ./texfiles/")
    os.system("rm -rf ./secureumBootcamp.???")

    print("\n\n" + 80*"#")
    print(BANNER7)