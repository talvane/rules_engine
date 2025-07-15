import React, { createContext, useState, useContext } from 'react';

const FieldsContext = createContext();

export const useFields = () => useContext(FieldsContext);

export const FieldsProvider = ({ children }) => {
  const [availableFields, setAvailableFields] = useState([
    { value: 'pontuacao_credito', label: 'Pontuação Crédito' },
    { value: 'renda_mensal', label: 'Renda Mensal' },
    { value: 'possui_divida_ativa', label: 'Possui Dívida Ativa' },
    { value: 'idade', label: 'Idade' },
  ]);

  const addNewField = (newFieldName) => {
    if (newFieldName && !availableFields.some(f => f.value === newFieldName)) {
      setAvailableFields(prev => [...prev, { value: newFieldName, label: newFieldName }]);
    }
  };

  return (
    <FieldsContext.Provider value={{ availableFields, addNewField }}>
      {children}
    </FieldsContext.Provider>
  );
};