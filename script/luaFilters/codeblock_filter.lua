function CodeBlock(elem)
  local latexCode = "\\begin{lstlisting}[language=Solidity,numbers=none]\n" .. elem.text .. "\n\\end{lstlisting}"
  return pandoc.RawBlock("latex", latexCode)
end
  
return {
  {
    CodeBlock = CodeBlock
  }
}  