import React from 'react';

const TrashCan = React.forwardRef(({ isOver }, ref) => {
  // Adiciona a classe 'active' se um nó estiver sendo arrastado sobre a lixeira
  const className = `trash-can ${isOver ? 'active' : ''}`;
  
  return (
    <div ref={ref} className={className}>
      🗑️
    </div>
  );
});

export default TrashCan;