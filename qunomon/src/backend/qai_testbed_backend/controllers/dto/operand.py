class Operand:
    def __init__(self, id_: int, operand_template_id: int, value: int, relational_operator_id: int) -> None:
        self.id = id_
        self.operand_template_id = operand_template_id
        self.value = value
        self.relational_operator_id = relational_operator_id


class PutOperandByTDEditReq:
    def __init__(self, operand: Operand) -> None:
        self.operand = operand
