from pydantic import BaseModel, Field

class Production(BaseModel):
    category: str = Field(..., description="Categoria do produto", example="VINHO DE MESA")
    product: str = Field(..., description="Tipo do produto", example="Tinto")
    quantity: float = Field(..., description="Quantidade anual", example="103916391")
    unit: str = Field(..., description="Unidade de medida usada como referência na quantidade", example="L")
    measurement: str = Field(..., description="Grandeza medida pela unidade", example="volume")
    year: int = Field(..., description="Ano de referência do dado informado", example="2020")

class Commercialization(BaseModel):
    category: str = Field(..., description="Categoria do produto", example="VINHO DE MESA")
    product: str = Field(..., description="Tipo do produto", example="Tinto")
    quantity: float = Field(..., description="Quantidade anual", example="103916391")
    unit: str = Field(..., description="Unidade de medida usada como referência na quantidade", example="L")
    measurement: str = Field(..., description="Grandeza medida pela unidade", example="volume")
    year: int = Field(..., description="Ano de referência do dado informado", example="2020")

class Processing(BaseModel):
    group: str = Field(..., description="Grupo da uva", example="Viníferas")
    category: str = Field(..., description="Categoria do cultivo", example="TINTAS")
    farm: str = Field(..., description="Casta de cultivo", example="TIAlicante BouschetNTAS")
    quantity: float = Field(..., description="Quantidade anual", example="2272985")
    unit: str = Field(..., description="Unidade de medida usada como referência na quantidade", example="Kg")
    measurement: str = Field(..., description="Grandeza medida pela unidade", example="mass")
    year: int = Field(..., description="Ano de referência do dado informado", example="2020")

class Importing_or_Exporting(BaseModel):
    group: str = Field(..., description="Grupo de derivados de uva", example="Vinhos de mesa")
    country: str = Field(..., description="País comercializante", example="Alemanha")
    quantity: float = Field(..., description="Quantidade comercializada", example="136992")
    unit: str = Field(..., description="Unidade de medida usada como referência na quantidade", example="Kg")
    measurement: str = Field(..., description="Grandeza medida pela unidade", example="mass")
    value: float = Field(..., description="Valor transacionado na comercialização", example="504168")
    currency: str = Field(..., description="Moeda representada no valor comercializado", example="US$")
    year: int = Field(..., description="Ano de referência do dado informado", example="2020")
